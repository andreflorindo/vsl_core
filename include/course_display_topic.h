/* Author: Andre Florindo*/
#ifndef COURSE_DISPLAY_TOPIC_H
#define COURSE_DISPLAY_TOPIC_H

// ROS
#include <ros/ros.h>
#include <vsl_core/PoseBuilder.h>

// Others
#include <eigen_conversions/eigen_msg.h>
#include <visualization_msgs/MarkerArray.h>
#include <eigen_stl_containers/eigen_stl_vector_container.h>

namespace vsl_motion_planning
{
const std::string VISUALIZE_TRAJECTORY_TOPIC = "visualize_trajectory_curve";
const double AXIS_LINE_LENGHT = 0.01;
const double AXIS_LINE_WIDTH = 0.01;

struct CourseDisplayConfiguration
{
    std::string world_frame;
    double min_point_distance; /* Minimum distance between consecutive trajectory points. */
};

class CourseDisplay
{
public:
    CourseDisplay();
    virtual ~CourseDisplay();
    visualization_msgs::MarkerArray markers_msg;

    void initTopic();
    void getPoseArray(geometry_msgs::PoseArray &course_poses);
    void publishPosesMarkers(const geometry_msgs::PoseArray &course_poses);

protected:
    CourseDisplayConfiguration config_;
    ros::NodeHandle nh_;
    ros::ServiceClient pose_builder_client_;
    ros::Publisher marker_publisher_;
};

} // namespace vsl_motion_planning

#endif