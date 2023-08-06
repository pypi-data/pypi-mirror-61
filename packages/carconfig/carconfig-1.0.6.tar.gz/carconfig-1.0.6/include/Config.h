#pragma once

#include <cstdint>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

#include "CANMessageType.h"
#include "Node.h"

class Config {

public:
    //std::map<uint32_t, std::shared_ptr<CANMessageType>> message_types_by_id;
    //std::map<std::string, std::shared_ptr<CANMessageType>> message_types_by_name;
    std::map<uint32_t, CANMessageType*> message_types_by_id;
    std::map<std::string, CANMessageType*> message_types_by_name;
    std::vector<CANMessageType*> message_types;
    std::vector<std::string> priority_names;
    std::map<std::string, int> priority_nums_by_name;
    std::vector<Node*> nodes;

    void load_from_file(std::string file_path);
    ~Config();
};
