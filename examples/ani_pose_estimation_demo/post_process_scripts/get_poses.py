import numpy as np
from pydrake.all import (
    DiagramBuilder,
    Simulator,
    MultibodyPlant,
    Parser,
    AddMultibodyPlantSceneGraph,
    RigidTransform,
)
# from pydrake.all import StartMeshcat -- Use this if you want the visualization
# from pydrake.visualization import MeshcatVisualizer

# --- 1. SETUP (Assuming you've already done this to run your simulation) ---

def setup_and_run_simulation(sdf_file_path, final_time):
    builder = DiagramBuilder()

    # Add MultibodyPlant and SceneGraph
    plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=1e-3)
    
    # Load your scene/objects
    parser = Parser(plant)
    # The ModelInstanceIndex is useful for identifying groups of bodies
    object1_instance = parser.AddModelFromFile(sdf_file_path, "object1")
    # Add other objects...
    
    # Weld the world to the ground frame
    plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("ground")) 
    
    plant.Finalize()

    # Connect to Meshcat if desired (uncomment if you need visualization)
    # meshcat = StartMeshcat()
    # MeshcatVisualizer.AddTo  (builder, scene_graph, meshcat)

    diagram = builder.Build()
    context = diagram.CreateDefaultContext()
    plant_context = plant.GetMutableSubsystemContext(context, plant)

    # Set initial state if necessary (e.g., non-zero start positions)
    # plant.SetFreeBodyPose(plant_context, 
    #                       plant.GetBodyByName("object1"), 
    #                       RigidTransform([0.0, 0.0, 0.5]))

    # Create and run the simulator
    simulator = Simulator(diagram, context)
    simulator.Initialize()
    print(f"Running simulation until t={final_time}...")
    simulator.AdvanceTo(final_time)
    print("Simulation finished.")

    return diagram, plant, simulator, [object1_instance] # Return the diagram and plant for querying

# --- 2. THE POSE QUERY FUNCTION ---

def get_final_poses(diagram, plant, simulator, model_instance_indices):
    """
    Queries the final pose (RigidTransform) for specified objects 
    after the simulation has completed.
    """
    
    # Get the final context from the simulator
    root_context = simulator.get_context()
    plant_context = plant.GetSubsystemContext(root_context, plant)
    
    final_poses = {}

    for instance in model_instance_indices:
        # Get the name of the object model instance
        model_name = plant.GetModelInstanceName(instance)
        
        # Get the main free-floating body for this model instance.
        # This assumes your object has a single free-floating base body.
        # This will be the body connected to the world by a floating joint.
        try:
            # Get the body corresponding to the model instance's base link
            body = plant.GetBodyByName(plant.GetModelInstanceName(instance), instance)
        except RuntimeError:
             # Fallback: if the object is complex, you may need a specific body name
             # For a simple block, the body name is often the same as the model name.
             body = plant.GetBodyByName(model_name) 

        # X_WB is the pose (RigidTransform) of the Body B in the World Frame W
        X_WB = plant.GetPoseInWorld(plant_context, body)
        
        # Extract components
        position = X_WB.translation()
        rotation_quat = X_WB.rotation().ToQuaternion()
        
        final_poses[model_name] = {
            "position": position,
            "quaternion": rotation_quat
        }
    
    return final_poses

# --- 3. MAIN EXECUTION ---

# ⚠️ Replace with your actual path and desired final time
# For stability, you often need to run for a few seconds (e.g., 5.0) 
# until objects settle due to gravity and friction.
MY_SDF_PATH = "/path/to/your/object_model.sdf" 
SETTLING_TIME = 5.0 

# Run the simulation
# diagram, plant, simulator, instances = setup_and_run_simulation(MY_SDF_PATH, SETTLING_TIME)

# Query the poses
# final_data = get_final_poses(diagram, plant, simulator, instances)

# Print the results
# for name, data in final_data.items():
#     print(f"\n--- Final Pose for Model: {name} ---")
#     print(f"Position (x, y, z): {data['position']}")
#     print(f"Orientation (Quat w, x, y, z): {data['quaternion'].w, data['quaternion'].x, data['quaternion'].y, data['quaternion'].z}")