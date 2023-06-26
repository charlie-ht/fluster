# Fluster - testing framework for decoders conformance
# Copyright (C) 2023, Igalia S.L.
#  Author: Charlie Turner <cturner@igalia.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <https://www.gnu.org/licenses/>.

import os
from fluster.codec import Codec, OutputFormat
from fluster.decoder import Decoder, register_decoder
from fluster.utils import file_checksum, run_command

class NvVkSampleDecoder(Decoder):
    '''Generic class for NvVkSample decoder'''
    binary = 'vk-video-dec-test'
    description = "NVIDIA Vulkan-accelerated video decoder"
    icd_override = None

    def __init__(self) -> None:
        super().__init__()
        self.name = f'NvVkSample-{self.codec.value}'
        self.description = f'NVIDIA Vulkan sample decoder for {self.codec.value}'

    def decode(
        self,
        input_filepath: str,
        output_filepath: str,
        output_format: OutputFormat,
        timeout: int,
        verbose: bool,
        keep_files: bool,
    ) -> str:
        '''Decodes input_filepath in output_filepath'''
        # pylint: disable=unused-argument
        cmd_env = ["env"]
        env_passthru = {'PATH', 'VK_ICD_FILENAMES', 'VK_LAYER_PATH', 'LD_LIBRARY_PATH', 'LIBVA_DRIVERS_PATH', 'LIBVA_DRIVER_NAME'}
        for k, v in os.environ.items():
            if k in env_passthru:
                cmd_env.append(f'{k}={v}')
            if k == 'VK_ICD_FILENAMES' and 'radeon' in v:
                # Hidden behind a feature flag for now
                cmd_env.append('RADV_PERFTEST=video_decode')

        cmd = cmd_env + [self.binary, "-i", input_filepath, "--noPresent", "-b", "-o", output_filepath]
        run_command(cmd, timeout=timeout, verbose=verbose)
        return file_checksum(output_filepath)

@register_decoder
class NvVkSampleH264Decoder(NvVkSampleDecoder):
    '''NvVkSample decoder for H.264'''
    codec = Codec.H264

@register_decoder
class NvVkSampleH265Decoder(NvVkSampleDecoder):
    '''NvVkSample decoder for H.265'''
    codec = Codec.H265

@register_decoder
class NvVkSampleAV1VulkanDecoder(NvVkSampleDecoder):
    '''NvVkSample decoder for AV1'''
    codec = Codec.AV1

