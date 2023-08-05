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

#include <stdint.h>
#include <unordered_map>
#include <map>
#include <vector>
#include <set>
#include "rev/CANSparkMaxFrames.h"

namespace rev {

typedef struct {
    frc_deviceType_t deviceTypeId;
    frc_manufacturer_t manufacturerId;
    uint16_t canId;   
    uint32_t uniqueId; 
} CANScanIdentifier;
  

inline bool operator<(const CANScanIdentifier& lhs, const CANScanIdentifier& rhs) {
        return std::tie(lhs.deviceTypeId, lhs.manufacturerId, lhs.canId, lhs.uniqueId) < 
        std::tie(rhs.deviceTypeId, rhs.manufacturerId, rhs.canId, rhs.uniqueId);
}

inline bool operator>(const CANScanIdentifier& lhs, const CANScanIdentifier& rhs) {
        return std::tie(lhs.deviceTypeId, lhs.manufacturerId, lhs.canId, lhs.uniqueId) >
                std::tie(rhs.deviceTypeId, rhs.manufacturerId, rhs.canId, rhs.uniqueId);
}

inline bool operator==(const CANScanIdentifier& lhs, const CANScanIdentifier& rhs) {
        return std::tie(lhs.deviceTypeId, lhs.manufacturerId, lhs.canId, lhs.uniqueId) ==
                std::tie(rhs.deviceTypeId, rhs.manufacturerId, rhs.canId, rhs.uniqueId);
}

class CANBusScanner {

public:
    CANBusScanner(int buffersize = 100);
    ~CANBusScanner();

    bool Start();
    void Stop();
    std::vector<CANScanIdentifier> CANBusScan();
    void RegisterDevice(std::string name, std::vector<uint32_t> validIds);

private:
    // Key is the name of the "filter" or device
    // Value is a vector of all valid message IDs that uniquely originate from that 
    // kind of device
    std::unordered_map<std::string, std::vector<uint32_t>> m_registeredDevices;
    std::map<uint16_t, std::string> m_lookUpMap;
    
    int m_streamBufferSize;
    uint32_t m_streamHandle;
};
} // namespace rev
