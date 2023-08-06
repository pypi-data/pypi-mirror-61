#include "Config.h"

#include <iostream>
#include <memory>
#include <string>
#include <set>

#include "yaml-cpp/yaml.h"

void Config::load_from_file(std::string file_path){
    YAML::Node config = YAML::LoadFile(file_path);

    YAML::Node can_format = config["CAN Format"];
    YAML::Node priority_levels = can_format["priority_levels"];


    /* Load priority levels */
    int max = 0;
    for(auto pair : priority_levels){
        int current = pair.second.as<int>();
        if(current > max) max = current;
    }
    this->priority_names.resize(max + 1);
    for(auto pair : priority_levels){
        this->priority_names[pair.second.as<int>()] = pair.first.as<std::string>();
        this->priority_nums_by_name[pair.first.as<std::string>()] = pair.second.as<int>();
    }
    /*----------------------*/


    YAML::Node nodes = can_format["nodes"];


    /* Generate set of reserved IDs */
    std::set<uint32_t> reserved_ids;

    for(auto pair : nodes){
        YAML::Node published = pair.second["publish"];
        for(auto name_and_info : published){
            YAML::Node info = name_and_info.second;
            if(info["id"]){
                reserved_ids.insert(info["id"].as<uint32_t>());
                //std::cout << "Reserved id:" << info["id"].as<uint32_t>() << std::endl;
            }
        }
    }
    /* ---------------------------- */


    /* Load node info */
    int node_id = 1;
    for(auto pair : nodes){
        Node *node = new Node();
        this->nodes.push_back(node);
        node->name = pair.first.as<std::string>();
        node->id = node_id;
        YAML::Node published = pair.second["publish"];
        for(auto name_and_info : published){
            //std::shared_ptr<CANMessageType> message_type = std::make_shared<CANMessageType>();
            CANMessageType *message_type = new CANMessageType();

            std::string name = name_and_info.first.as<std::string>();
            YAML::Node info = name_and_info.second;

            message_type->priority_num = priority_levels[info["priority"].as<std::string>()].as<int>();

            uint32_t id = 0;
            if(!info["id"]){
                for(int seq_id = 0; seq_id < 0xFFFF; seq_id++){
                    uint32_t proposed_id = (message_type->priority_num << 24) | (node->id << 16) | seq_id;
                    if(reserved_ids.find(proposed_id) == reserved_ids.end()){
                        id = proposed_id;
                        reserved_ids.insert(id);
                        //std::cout << "Assigning: " << name << " -> 0x" << std::hex << proposed_id << std::dec << std::endl;
                        break;
                    }
                }
            }else{
                id = info["id"].as<uint32_t>();
            }

            if(info["expected_interval"]){
                message_type->expected_interval = info["expected_interval"].as<int>();
            }else{
                message_type->expected_interval = -1;
            }

            message_type->name = name;
            message_type->id = id;
            message_type->publisher = node;

            /* Load field type data */
            YAML::Node fields = info["fields"];
            for(auto field_name_and_info : fields){

                std::string field_name = field_name_and_info.first.as<std::string>();
                YAML::Node field_info = field_name_and_info.second;

                FieldType *field = FieldType::create_field_type(field_name, field_info);
                
                message_type->fields.push_back(field);
            }
            /* -------------------- */
            
            this->message_types.push_back(message_type);
            this->message_types_by_id[id] = message_type;
            this->message_types_by_name[name] = message_type;
            node->published.push_back(message_type);
        }

        node_id += 1;
    }

}

Config::~Config(){
    for(CANMessageType *message_type : this->message_types){
        delete message_type;
    }

    for(Node *node : this->nodes){
        delete node;
    }
}
