#pragma once

#include <vector>

#include "FieldType.h"

class Node;

class CANMessageType{
    public:
        static CANMessageType UNKNOWN;
        uint32_t id;
        std::string name;
        std::vector<FieldType*> fields;
        int expected_interval;
        int priority_num;
        Node *publisher;
        
        CANMessageType();
        CANMessageType(std::string name);
        ~CANMessageType();
};
