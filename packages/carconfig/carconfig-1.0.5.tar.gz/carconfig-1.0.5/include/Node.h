#pragma once

#include <vector>

#include "CANMessageType.h"

class Node {

    public:
        int id;
        std::string name;
        std::vector<CANMessageType*> published;
        std::vector<CANMessageType*> subscribed;

};
