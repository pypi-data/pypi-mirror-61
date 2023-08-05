/*
 * Copyright (c) 2018-2019 REV Robotics
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of REV Robotics nor the names of its
 *    contributors may be used to endorse or promote products derived from
 *    this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#pragma once

#include "rev/CANSparkMaxDriver.h"

extern "C" {

typedef enum {
    c_SparkMax_kBusVoltage = 0,
    c_SparkMax_kOutputCurrent,
    c_SparkMax_kSensorVelocity,
    c_SparkMax_kSensorPosition,
    c_SparkMax_kIAccum,
    c_SparkMax_kAppliedOutput,
    c_SparkMax_kMotorTemp,
    c_SparkMax_kFaults,
    c_SparkMax_kStickyFaults,
    c_SparkMax_kAnalogVoltage,
    c_SparkMax_kAnalogPosition, 
    c_SparkMax_kAnalogVelocity,
    c_SparkMax_kAltEncPosition,
    c_SparkMax_kAltEncVelocity,
    c_SparkMax_kTotalStreams
} c_SparkMax_TelemetryID;

typedef struct {
    c_SparkMax_TelemetryID id;
    float value = 0;
    uint64_t timestamp = 0;
    const char* name;
    const char* units;
    float lowerBnd;
    float upperBnd;
} c_SparkMax_TelemetryMessage;

// Streamable 
c_SparkMax_ErrorCode c_SparkMax_ReadTelemetryStream(c_SparkMax_handle handle, uint32_t telemetryHandle, c_SparkMax_TelemetryMessage* messages, 
                                                    c_SparkMax_TelemetryID* ids, uint32_t numOfStreams);
c_SparkMax_ErrorCode c_SparkMax_OpenTelemetryStream(c_SparkMax_handle handle, uint32_t* telemetryHandle);
c_SparkMax_ErrorCode c_SparkMax_CloseTelemetryStream(c_SparkMax_handle handle, uint32_t telemetryHandle);
c_SparkMax_ErrorCode c_SparkMax_ListTelemetryStream(c_SparkMax_handle handle, c_SparkMax_TelemetryMessage* messages);

}