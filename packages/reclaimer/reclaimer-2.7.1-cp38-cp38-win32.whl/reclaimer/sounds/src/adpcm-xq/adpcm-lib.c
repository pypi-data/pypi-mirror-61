////////////////////////////////////////////////////////////////////////////
//                           **** ADPCM-XQ ****                           //
//                  Xtreme Quality ADPCM Encoder/Decoder                  //
//                    Copyright (c) 2015 David Bryant.                    //
//                          All Rights Reserved.                          //
//      Distributed under the BSD Software License (see license.txt)      //
////////////////////////////////////////////////////////////////////////////

#include <stdlib.h>
#include <string.h>

#include "adpcm-lib.h"

/* This module encodes and decodes 4-bit ADPCM (DVI/IMA varient). ADPCM data is divided
 * into independently decodable blocks that can be relatively small. The most common
 * configuration is to store 505 samples into a 256 byte block, although other sizes are
 * permitted as long as the number of samples is one greater than a multiple of 8. When
 * multiple channels are present, they are interleaved in the data with an 8-sample
 * interval. 
 */

/********************************* 4-bit ADPCM encoder ********************************/

#define CLIP(data, min, max) \
if ((data) > (max)) data = max; \
else if ((data) < (min)) data = min;

struct adpcm_channel {
    int32_t pcmdata;                        // current PCM value
    int32_t error, weight, history [MAX_AUDIO_CHANNEL_COUNT];     // for noise shaping
    int8_t index;                           // current index into step size table
};

struct adpcm_context {
    struct adpcm_channel channels [MAX_AUDIO_CHANNEL_COUNT];
    int num_channels, lookahead, noise_shaping;
};

/* Create ADPCM encoder context with given number of channels.
 * The returned pointer is used for subsequent calls. Note that
 * even though an ADPCM encoder could be set up to encode frames
 * independently, we use a context so that we can use previous
 * data to improve quality (this encoder might not be optimal
 * for encoding independent frames).
 */

void *adpcm_create_context (int num_channels, int lookahead, int noise_shaping, int32_t *initial_deltas)
{
    struct adpcm_context *pcnxt = malloc (sizeof (struct adpcm_context));
    int ch, i;

    memset (pcnxt, 0, sizeof (struct adpcm_context));
    pcnxt->noise_shaping = noise_shaping;
    pcnxt->num_channels = num_channels;
    pcnxt->lookahead = lookahead;

    // given the supplied initial deltas, search for and store the closest index

    for (ch = 0; ch < num_channels; ++ch)
        for (i = 0; i <= 88; i++)
            if (i == 88 || initial_deltas [ch] < ((int32_t) step_table [i] + step_table [i+1]) / 2) {
                pcnxt->channels [ch].index = i;
                break;
            }

    return pcnxt;
}

/* Free the ADPCM encoder context.
 */

void adpcm_free_context (void *p)
{
    struct adpcm_context *pcnxt = (struct adpcm_context *) p;

    free (pcnxt);
}

static void set_decode_parameters (struct adpcm_context *pcnxt, int32_t *init_pcmdata, int8_t *init_index)
{
    int ch;

    for (ch = 0; ch < pcnxt->num_channels; ch++) {
        pcnxt->channels[ch].pcmdata = init_pcmdata[ch];
        pcnxt->channels[ch].index = init_index[ch];
    }
}

static void get_decode_parameters (struct adpcm_context *pcnxt, int32_t *init_pcmdata, int8_t *init_index)
{
    int ch;

    for (ch = 0; ch < pcnxt->num_channels; ch++) {
        init_pcmdata[ch] = pcnxt->channels[ch].pcmdata;
        init_index[ch] = pcnxt->channels[ch].index;
    }
}

static double minimum_error (const struct adpcm_channel *pchan, int nch, int32_t csample, const int16_t *sample, int depth, int *best_nibble)
{
    int32_t delta = csample - pchan->pcmdata;
    struct adpcm_channel chan = *pchan;
    int step = step_table[chan.index];
    int trial_delta = (step >> 3);
    int nibble, nibble2;
    double min_error;

    if (delta < 0) {
        int mag = (-delta << 2) / step;
        nibble = 0x8 | (mag > 7 ? 7 : mag);
    }
    else {
        int mag = (delta << 2) / step;
        nibble = mag > 7 ? 7 : mag;
    }

    if (nibble & 1) trial_delta += (step >> 2);
    if (nibble & 2) trial_delta += (step >> 1);
    if (nibble & 4) trial_delta += step;
    if (nibble & 8) trial_delta = -trial_delta;

    chan.pcmdata += trial_delta;
    CLIP(chan.pcmdata, -32768, 32767);
    if (best_nibble) *best_nibble = nibble;
    min_error = (double) (chan.pcmdata - csample) * (chan.pcmdata - csample);

    if (depth) {
        chan.index += index_table[nibble & 0x07];
        CLIP(chan.index, 0, 88);
        min_error += minimum_error (&chan, nch, sample [nch], sample + nch, depth - 1, NULL);
    }
    else
        return min_error;

    for (nibble2 = 0; nibble2 <= 0xF; ++nibble2) {
        double error;

        if (nibble2 == nibble)
            continue;

        chan = *pchan;
        trial_delta = (step >> 3);

        if (nibble2 & 1) trial_delta += (step >> 2);
        if (nibble2 & 2) trial_delta += (step >> 1);
        if (nibble2 & 4) trial_delta += step;
        if (nibble2 & 8) trial_delta = -trial_delta;

        chan.pcmdata += trial_delta;
        CLIP(chan.pcmdata, -32768, 32767);

        error = (double) (chan.pcmdata - csample) * (chan.pcmdata - csample);

        if (error < min_error) {
            chan.index += index_table[nibble2 & 0x07];
            CLIP(chan.index, 0, 88);
            error += minimum_error (&chan, nch, sample [nch], sample + nch, depth - 1, NULL);

            if (error < min_error) {
                if (best_nibble) *best_nibble = nibble2;
                min_error = error;
            }
        }
    }

    return min_error;
}

static uint8_t encode_sample (struct adpcm_context *pcnxt, int ch, const int16_t *sample, int num_samples)
{
    struct adpcm_channel *pchan = pcnxt->channels + ch;
    int32_t csample = *sample;
    int depth = num_samples - 1, nibble;
    int step = step_table[pchan->index];
    int trial_delta = (step >> 3);

    if (pcnxt->noise_shaping == NOISE_SHAPING_DYNAMIC) {
        int32_t sam = (3 * pchan->history [0] - pchan->history [1]) >> 1;
        int32_t temp = csample - (((pchan->weight * sam) + 512) >> 10);
        int32_t shaping_weight;

        if (sam && temp) pchan->weight -= (((sam ^ temp) >> 29) & 4) - 2;
        pchan->history [1] = pchan->history [0];
        pchan->history [0] = csample;

        shaping_weight = (pchan->weight < 256) ? 1024 : 1536 - (pchan->weight * 2);
        temp = -((shaping_weight * pchan->error + 512) >> 10);

        if (shaping_weight < 0 && temp) {
            if (temp == pchan->error)
                temp = (temp < 0) ? temp + 1 : temp - 1;

            pchan->error = -csample;
            csample += temp;
        }
        else
            pchan->error = -(csample += temp);
    }
    else if (pcnxt->noise_shaping == NOISE_SHAPING_STATIC)
        pchan->error = -(csample -= pchan->error);

    if (depth > pcnxt->lookahead)
        depth = pcnxt->lookahead;

    minimum_error (pchan, pcnxt->num_channels, csample, sample, depth, &nibble);

    if (nibble & 1) trial_delta += (step >> 2);
    if (nibble & 2) trial_delta += (step >> 1);
    if (nibble & 4) trial_delta += step;
    if (nibble & 8) trial_delta = -trial_delta;

    pchan->pcmdata += trial_delta;
    pchan->index += index_table[nibble & 0x07];
    CLIP(pchan->index, 0, 88);
    CLIP(pchan->pcmdata, -32768, 32767);

    if (pcnxt->noise_shaping)
        pchan->error += pchan->pcmdata;

    return nibble;
}

static void encode_chunks (struct adpcm_context *pcnxt, uint8_t **outbuf, size_t *outbufsize, const int16_t **inbuf, int inbufcount)
{
    const int16_t *pcmbuf;
    int chunks, ch, i;

    //chunks = (inbufcount - 1) / 8;
    chunks = inbufcount / 8;  // we want to encode multiples of 8 samples per block.
    *outbufsize += (chunks * 4) * pcnxt->num_channels;

    while (chunks--)
    {
        for (ch = 0; ch < pcnxt->num_channels; ch++)
        {
            pcmbuf = *inbuf + ch;

            for (i = 0; i < 4; i++) {
                **outbuf = encode_sample (pcnxt, ch, pcmbuf, chunks * 8 + (3 - i) * 2 + 2);
                pcmbuf += pcnxt->num_channels;
                **outbuf |= encode_sample (pcnxt, ch, pcmbuf, chunks * 8 + (3 - i) * 2 + 1) << 4;
                pcmbuf += pcnxt->num_channels;
                (*outbuf)++;
            }
        }

        *inbuf += 8 * pcnxt->num_channels;
    }
}

/* Encode a block of 16-bit PCM data into 4-bit ADPCM.
 *
 * Parameters:
 *  p               the context returned by adpcm_begin()
 *  outbuf          destination buffer
 *  outbufsize      pointer to variable where the number of bytes written
 *                   will be stored
 *  inbuf           source PCM samples
 *  inbufcount      number of composite PCM samples provided (note: this is
 *                   the total number of 16-bit samples divided by the number
 *                   of channels)
 *
 * Returns 1 (for success as there is no error checking)
 */

int adpcm_encode_block (void *p, uint8_t *outbuf, size_t *outbufsize, const int16_t *inbuf, int inbufcount)
{
    struct adpcm_context *pcnxt = (struct adpcm_context *) p;
    int32_t init_pcmdata[MAX_AUDIO_CHANNEL_COUNT];
    int8_t init_index[MAX_AUDIO_CHANNEL_COUNT];
    int ch;

    *outbufsize = 0;

    if (!inbufcount)
        return 1;

    get_decode_parameters(pcnxt, init_pcmdata, init_index);

    for (ch = 0; ch < pcnxt->num_channels; ch++) {
        init_pcmdata[ch] = *inbuf++;
        outbuf[0] = init_pcmdata[ch] & 0xFF;
        outbuf[1] = (init_pcmdata[ch] >> 8) & 0xFF;
        outbuf[2] = init_index[ch];
        outbuf[3] = 0;

        outbuf += 4;
        *outbufsize += 4;
    }

    set_decode_parameters(pcnxt, init_pcmdata, init_index);
    encode_chunks (pcnxt, &outbuf, outbufsize, &inbuf, inbufcount);

    return 1;
}