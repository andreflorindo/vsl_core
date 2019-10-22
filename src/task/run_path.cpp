#include <vsl_planner.h>

/* MOVE HOME
  Goal:
  - Translate the result into a type that ROS understands
    - Move the robot to from its current location to the first point in the robot path.
    - Execute the robot path.
*/

namespace vsl_motion_planning
{

void VSLPlanner::runPath(const std::vector<descartes_core::TrajectoryPtPtr> &path)
{

  // creating move group to move the arm in free space
  moveit::planning_interface::MoveGroupInterface move_group(config_.group_name);
  move_group.setPlannerId(PLANNER_ID);

  // creating goal joint pose to start of the path
  std::vector<double> seed_pose(robot_model_ptr_->getDOF());
  std::vector<double> start_pose;

  descartes_core::TrajectoryPtPtr first_point_ptr = path[0];
  first_point_ptr->getNominalJointPose(seed_pose, *robot_model_ptr_, start_pose);

  // moving arm to joint goal by using another planner, for example RRT
  move_group.setJointValueTarget(start_pose);
  move_group.setPlanningTime(10.0f);
  moveit_msgs::MoveItErrorCodes result = move_group.move();
  if (result.val != result.SUCCESS)
  {
    ROS_ERROR_STREAM("Move to start joint pose failed");
    exit(-1);
  }

  // creating Moveit trajectory from Descartes Trajectory
  moveit_msgs::RobotTrajectory moveit_traj;
  fromDescartesToMoveitTrajectory(path, moveit_traj.joint_trajectory);

  /////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////

  sensor_msgs::JointState joint_pose;

  int num_joints = moveit_traj.joint_trajectory.points[0].positions.size();
  int num_points = moveit_traj.joint_trajectory.points.size();

  std::vector<std::vector<double>> buffer_position;
  std::vector<std::vector<double>> buffer_velocity;

  buffer_position.resize(num_joints, std::vector<double>(num_points));
  buffer_velocity.resize(num_joints, std::vector<double>(num_points));

  for (int i = 0; i < num_joints; i++)
  {
    for (int j = 0; j < num_points; j++)
    {
      buffer_position[i][j] = moveit_traj.joint_trajectory.points[j].positions[i];
      buffer_velocity[i][j] = moveit_traj.joint_trajectory.points[j].velocities[i];
      // joint_pose.position[i] = moveit_traj.joint_trajectory.points[j].positions[i];
      // joint_pose.velocity[i] = moveit_traj.joint_trajectory.points[j].velocities[i];
      joint_pose.position.push_back(buffer_position[0][j]);
      joint_pose.velocity.push_back(buffer_velocity[0][j]);
    }

    joint_pose.header = moveit_traj.joint_trajectory.header;
    joint_pose.name.push_back(moveit_traj.joint_trajectory.joint_names[i]);
    

    // joint_pose.position.push_back(buffer_position[i]);
    // joint_pose.velocity.push_back(buffer_velocity[i]);
  }

  //joint_pose_publisher_.publish(joint_pose);
  joint_pose_publisher_.publish(moveit_traj.joint_trajectory);

  ////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////

  // sending robot path to server for execution
  moveit_msgs::ExecuteTrajectoryGoal goal;
  goal.trajectory = moveit_traj;

  ROS_INFO_STREAM("Robot path sent for execution");
  if (moveit_run_path_client_ptr_->sendGoalAndWait(goal) == actionlib::SimpleClientGoalState::SUCCEEDED)
  {
    ROS_INFO_STREAM("Robot path execution completed");
  }
  else
  {
    ROS_ERROR_STREAM("Failed to run robot path with error " << *moveit_run_path_client_ptr_->getResult());
    exit(-1);
  }

  ROS_INFO_STREAM("Task '" << __FUNCTION__ << "' completed");
}

void VSLPlanner::fromDescartesToMoveitTrajectory(const std::vector<descartes_core::TrajectoryPtPtr> &input_traj,
                                                 trajectory_msgs::JointTrajectory &traj)
{
  //  // Fill out information about our trajectory
  traj.header.stamp = ros::Time::now();
  traj.header.frame_id = config_.world_frame;
  traj.joint_names = config_.joint_names;

  descartes_utilities::toRosJointPoints(*robot_model_ptr_, input_traj, 0.4, traj.points);
  addVel(traj);
  // addAcc(traj);
}

void VSLPlanner::addVel(trajectory_msgs::JointTrajectory &traj) //Velocity of the joints
{
  if (traj.points.size() < 3)
    return;

  auto n_joints = traj.points.front().positions.size();

  for (auto i = 0; i < n_joints; ++i)
  {
    traj.points[0].velocities[i] = 0.0f;
    traj.points[traj.points.size()-1].velocities[i] = 0.0f;
    for (auto j = 1; j < traj.points.size() - 1; j++)
    {
      // For each point in a given joint
      //Finite difference, first order, central. Gives the average velocity, not conservative
      double delta_theta = -traj.points[j - 1].positions[i] + traj.points[j + 1].positions[i];
      double delta_time = -traj.points[j - 1].time_from_start.toSec() + traj.points[j + 1].time_from_start.toSec();
      double v = delta_theta / delta_time;
      traj.points[j].velocities[i] = v;
    }

  }
}

// void VSLPlanner::addAcc(trajectory_msgs::JointTrajectory &traj) //Velocity of the joints
// {
//   if (traj.points.size() < 3)
//     return;

//   auto n_joints = traj.points.front().positions.size();

//   for (auto i = 0; i < n_joints; ++i)
//   {

//     for (auto j = 1; j < traj.points.size(); j++)
//     {
//       // For each point in a given joint
//       //Finite difference, first order, central. Gives the average velocity, not conservative
//       double delta_velocity = -traj.points[j - 1].velocities[i] + traj.points[j + 1].velocities[i];
//       double delta_time = -traj.points[j - 1].time_from_start.toSec() + traj.points[j + 1].time_from_start.toSec();
//       double a = delta_velocity / delta_time;
//       traj.points[j].accelerations[i] = a;
//     }

//   }
// }


// void VSLPlanner::addVel(trajectory_msgs::JointTrajectory &traj) //Velocity of the joints
// {
//   if (traj.points.size() < 3)
//     return;

//   auto n_joints = traj.points.front().positions.size();

//   for (auto i = 0; i < n_joints; ++i)
//   {
//     traj.points[0].velocities[i] = 0.0f;
//     //traj.points[traj.points.size()-1].velocities[i] = 0.0f;

//     for (auto j = 1; j < traj.points.size(); j++)
//     {
//       // For each point in a given joint
//       //Finite difference, first order, regressive
//       double delta_theta = traj.points[j].positions[i] - traj.points[j - 1].positions[i];
//       double delta_time = traj.points[j].time_from_start.toSec() - traj.points[j - 1].time_from_start.toSec();
//       double v = delta_theta / delta_time;
//       traj.points[j].velocities[i] = v;
//     }

//   }
// }

// void VSLPlanner::addAcc(trajectory_msgs::JointTrajectory &traj) //Velocity of the joints
// {
//   if (traj.points.size() < 3)
//     return;

//   auto n_joints = traj.points.front().positions.size();

//   for (auto i = 0; i < n_joints; ++i)
//   {
//     traj.points[0].accelerations[i] = 0.0f;
//     //traj.points[traj.points.size()-1].velocities[i] = 0.0f;

//     for (auto j = 1; j < traj.points.size(); j++)
//     {
//       // For each point in a given joint
//       //Finite difference, first order, regressive
//       double delta_velocity = traj.points[j].velocities[i] - traj.points[j - 1].velocities[i];
//       double delta_time = traj.points[j].time_from_start.toSec() - traj.points[j - 1].time_from_start.toSec();
//       double a = delta_velocity / delta_time;
//       traj.points[j].accelerations[i] = a;
//     }

//   }
// }


// void VSLPlanner::getJacobian()
// {
//   Eigen::Vector3d reference_point_position(0.0, 0.0, 0.0);
//   Eigen::MatrixXd jacobian;

//   robot_model_ptr_->getJacobian(reference_point_position, jacobian);

//   ROS_INFO_STREAM("Jacobian: \n"
//                   << jacobian << "\n");
// }

} // namespace vsl_motion_planning
