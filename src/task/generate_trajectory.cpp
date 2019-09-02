#include <vsl_planner.h>

/* GENERATE TRAJECTORY
  Goal:
    - Create a Descartes Trajectory from an array of poses.
    - Create trajectory points that are free to rotate about the tool's z axis
*/

namespace vsl_motion_planning
{

void VSLPlanner::generateTrajectory(EigenSTL::vector_Isometry3d *PosesPtr, std::vector<descartes_core::TrajectoryPtPtr> &traj)
{
    using namespace descartes_core;
    using namespace descartes_trajectory;
    
    EigenSTL::vector_Isometry3d poses;
    PosesPtr=&poses;

    // creating descartes trajectory points
    traj.clear();
    traj.reserve(poses.size());
    for (unsigned int i = 0; i < poses.size(); i++)
    {
        const Eigen::Isometry3d &single_pose = poses[i];

        /*  Create AxialSymetricPt objects in order to define a trajectory cartesian point with
            rotational freedom about the tool's z axis.
         */

        descartes_core::TrajectoryPtPtr pt = descartes_core::TrajectoryPtPtr(
            new descartes_trajectory::AxialSymmetricPt(single_pose, ORIENTATION_INCREMENT, descartes_trajectory::AxialSymmetricPt::FreeAxis::Z_AXIS));

        // saving points into trajectory
        traj.push_back(pt);
    }

    ROS_INFO_STREAM("Task '" << __FUNCTION__ << "' completed");
}

}
