/*
 *  Copyright (c) 2016 The WebRTC project authors. All Rights Reserved.
 *
 *  Use of this source code is governed by a BSD-style license
 *  that can be found in the LICENSE file in the root of the source
 *  tree. An additional intellectual property rights grant can be found
 *  in the file PATENTS.  All contributing project authors may
 *  be found in the AUTHORS file in the root of the source tree.
 */

#ifndef COMMON_AUDIO_MOCKS_MOCK_SMOOTHING_FILTER_H_
#define COMMON_AUDIO_MOCKS_MOCK_SMOOTHING_FILTER_H_

#include "common_audio/smoothing_filter.h"
#include "test/gmock.h"

namespace webrtc {

class MockSmoothingFilter : public SmoothingFilter {
 public:
  MOCK_METHOD1(AddSample, void(float));
  MOCK_METHOD0(GetAverage, absl::optional<float>());
  MOCK_METHOD1(SetTimeConstantMs, bool(int));
};

}  // namespace webrtc

#endif  // COMMON_AUDIO_MOCKS_MOCK_SMOOTHING_FILTER_H_
