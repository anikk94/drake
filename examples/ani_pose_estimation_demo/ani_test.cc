#include <iostream>

#include <gflags/gflags.h>


// #include "drake/examples/pendulum/pendulum_geometry.h"
// #include "drake/examples/pendulum/pendulum_plant.h"
#include "drake/geometry/drake_visualizer.h"
#include "drake/systems/analysis/simulator.h"
#include "drake/systems/framework/diagram.h"
#include "drake/systems/framework/diagram_builder.h"
#include "drake/systems/primitives/constant_vector_source.h"

#include <drake/systems/lcm/lcm_interface_system.h>
#include "drake/systems/lcm/lcm_subscriber_system.h"
#include "drake/lcmt_drake_signal.hpp"




namespace drake {
namespace examples {

        namespace {
            
            int DoMain(){
                std::cout << "DoMain()" << std::endl;
                
                
                systems::DiagramBuilder<double> builder;
                auto lcm = builder.AddSystem<systems::lcm::LcmInterfaceSystem>();
                
                const std::string channelName="DRAKE_VIEWER_DRAW";
                
                auto subscriber = builder.AddSystem(
                    systems::lcm::LcmSubscriberSystem::Make<lcmt_drake_signal>(channelName, lcm));
                    
                subscriber->set_name("ani_subscriber");



                std::cout << subscriber->GetInternalMessageCount() << std::endl;

                // builder.Connect(
                //     subscriber->get_output_port(),

                // );

                    return 0;
                };
                
                
            }
        }
    }


int main(int argc, char* argv[]){
    gflags::ParseCommandLineFlags(&argc,&argv,true);
    return drake::examples::DoMain();
}
