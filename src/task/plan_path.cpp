#include <vsl_planner.h>

/* PLAN AND RUN
  Goal:
    - Plan a robot path from a trajectory using the path planner
    - Observe how to modify the start and end points in the trajectory so that
      unique joint poses at those points are used instead.  Skipping this step would cause planning
      for multiple path possibilities (multiple combinations of start and end), which
      could take a very long time.
*/

namespace vsl_motion_planning
{

void VSLPlanner::planPath(std::vector<descartes_core::TrajectoryPtPtr>& input_traj, 
                          std::vector<descartes_core::TrajectoryPtPtr>& output_path)
{

  //modifying start and end points such that are close to seed_pose
  std::vector<double> start_pose, end_pose;
  if(input_traj.front()->getClosestJointPose(config_.seed_pose,*robot_model_ptr_,start_pose) &&
      input_traj.back()->getClosestJointPose(config_.seed_pose,*robot_model_ptr_,end_pose))
  {
    ROS_INFO_STREAM("Setting trajectory start and end to JointTrajectoryPts");

    // Creating Start JointTrajectoryPt from start joint pose
    descartes_core::TrajectoryPtPtr start_joint_point = descartes_core::TrajectoryPtPtr(
        new descartes_trajectory::JointTrajectoryPt(start_pose));

    // Creating End JointTrajectoryPt from end joint pose
    descartes_core::TrajectoryPtPtr end_joint_point = descartes_core::TrajectoryPtPtr(
        new descartes_trajectory::JointTrajectoryPt(end_pose));

    // Modifying start and end of the trajectory.
    input_traj[0] = start_joint_point;
    input_traj[input_traj.size() - 1 ] = end_joint_point;
  }
  else
  {
    ROS_ERROR_STREAM("Failed to find closest joint pose to seed pose at the start or end of trajectory");
    exit(-1);
  }

  // planning robot path
  bool succeeded = planner_.planPath(input_traj);

  if (succeeded)
  {
    ROS_INFO_STREAM("Valid path was found");
  }
  else
  {
    ROS_ERROR_STREAM("Could not solve for a valid path");
    exit(-1);
  }

  // retrieving robot path
  succeeded = planner_.getPath(output_path);

  if(!succeeded || output_path.empty())
  {
    ROS_ERROR_STREAM("Failed to retrieve robot path");
  }

  ROS_INFO_STREAM("Task '"<<__FUNCTION__<<"' completed");
}

}


