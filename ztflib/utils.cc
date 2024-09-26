#include <iostream>
#include <string>
#include <vector>
#include <sys/stat.h>
#include <unistd.h>
#include <fstream>
#include <iostream>
#include <sstream>

std::vector<std::string> split(const std::string &str, const char &delimiter) {
  std::vector<std::string> tokens;
  std::string token;
  std::istringstream tokenStream(str);

  while (getline(tokenStream, token, delimiter)) {
    tokens.push_back(token);
  }

  return tokens;
}


bool endsWith(const std::string &str, const std::string &suffix) {
  if (suffix.length() > str.length()) {
    return false;
  }
  return (str.rfind(suffix) == (str.length() - suffix.length()));
}

bool startsWith(const std::string &str,
                              const std::string &suffix) {
  if (suffix.length() > str.length()) {
    return false;
  }
  return (str.find(suffix) == 0);
}

std::string rstrip(std::string str, const std::string &delimiter) {
  while (endsWith(str, delimiter)) {
    str = str.substr(0, str.size() - delimiter.size());
  }
  return str;
}

std::string lstrip(std::string str, const std::string &delimiter) {
  while (startsWith(str, delimiter)) {
    str = str.substr(delimiter.size());
  }
  return str;
}

std::string join(const std::vector<std::string> &vec,
                               const std::string &delimiter) {
  std::string result;
  for (size_t i = 0; i < vec.size(); ++i) {
    if (i > 0) {
      result += delimiter;
    }
    result += vec[i];
  }
  return result;
}

double round(double num, const int &precision){
    double temp = std::pow(10, precision + 1);
    long long p1 = num;
    long long p2 = (num - p1) * temp;
    int mod = p2 % 10;
    if (mod >= 5) p2 += 10;
    p2 -= mod;
    double res = p1 + p2 / temp;
    return res;
}

std::string timeConvert(unsigned int secs) {
  // 假设时间戳的秒数为secs
  time_t ts = static_cast<time_t>(secs);
  // ts=ts-28800;//UTC转化RTC默认-8小时
  // 将时间戳的秒数转换为time_t类型
  struct tm *tm_info =
      localtime(&ts); // 将time_t类型的时间转换为tm结构体类型的时间，本地时间
  char time_str[26]; // 定义一个字符数组来存储转换后的时间字符串
  strftime(time_str, 26, "%Y-%m-%d %H:%M:%S",
           tm_info); // 使用strftime函数格式化输出时间字符串
  // std::cout << " rosbagtime: " << time_str << std::endl;
  return time_str;
}


typedef struct {
  double yaw, pitch, roll;
} EulerAngle;

std::vector<double> eulerToQuaternion(EulerAngle angles) {
  // 将角度转换为弧度
  double thetaYaw = angles.yaw * 0.5;
  double thetaPitch = angles.pitch * 0.5;
  double thetaRoll = angles.roll * 0.5;
  // 计算三个轴的正弦和余弦值
  double cy = cos(thetaYaw);
  double sy = sin(thetaYaw);
  double cp = cos(thetaPitch);
  double sp = sin(thetaPitch);
  double cr = cos(thetaRoll);
  double sr = sin(thetaRoll);
  // 计算四元数的四个分量
  w = cy * cp * cr + sy * sp * sr;
  x = cy * cp * sr - sy * sp * cr;
  y = sy * cp * sr + cy * sp * cr;
  z = sy * cp * cr - cy * sp * sr;
  return {w, x, y, z};
}
bool fileExists(const std::string &file_name) { return access(file_name.c_str(), F_OK) != -1; }

bool creatNewFolder(const std::string &folder_name) {
    auto layers = split(folder_name, '/');
    std::string root;
    if(folder_name[0] == '/')root = "";
    else root = ".";
    bool flag = false;
    for(auto layer: layers){
      if(layer == "")continue;
      root += "/" + layer;
      if (access(root.c_str(), 0) == -1){
          if (mkdir(root.c_str(), S_IRWXU | S_IRWXG | S_IRWXO) == -1)continue;
          else flag = true;
      }
    }
    if (!flag)std::cout << "fail to creat new folder " << folder_name << std::endl;
    return flag;
}

std::string pathJoin(const std::vector<std::string> &vec)
{
    std::string result_path;
    std::string delimiter = "/";
    for (int i = 0; i < vec.size(); ++i)
    {
        std::string curr_dir = rstrip(vec[i], delimiter);
        if (i > 0)
        {
            result_path += delimiter;
            curr_dir = lstrip(curr_dir, delimiter);
        }
        result_path += curr_dir;
    }
    return result_path;
}

geometry_msgs::Quaternion eulerToQuaternion(const float& yaw, const float& pitch = 0, const float& roll = 0)
{
    geometry_msgs::Quaternion quaternion;

    double thetaYaw   = yaw * 0.5;
    double thetaPitch = pitch * 0.5;
    double thetaRoll  = roll * 0.5;

    // 计算三个轴的正弦和余弦值
    double cy = cos(thetaYaw);
    double sy = sin(thetaYaw);
    double cp = cos(thetaPitch);
    double sp = sin(thetaPitch);
    double cr = cos(thetaRoll);
    double sr = sin(thetaRoll);

    // 计算四元数的四个分量
    quaternion.w = cy * cp * cr + sy * sp * sr;
    quaternion.x = cy * cp * sr - sy * sp * cr;
    quaternion.y = sy * cp * sr + cy * sp * cr;
    quaternion.z = sy * cp * cr - cy * sp * sr;

    return quaternion;
}

void calCornerPoint(
    geometry_msgs::Point& res_point, const geometry_msgs::Point& tmp_point, const geometry_msgs::Point& center_point,
    const geometry_msgs::Quaternion& q)
{
    res_point.x = tmp_point.x * (q.w * q.w + q.x * q.x - q.y * q.y - q.z * q.z) +
                  tmp_point.y * 2 * (q.x * q.y - q.w * q.z) + tmp_point.z * 2 * (q.w * q.y + q.x * q.z) +
                  center_point.x;
    res_point.y = tmp_point.x * 2 * (q.w * q.z + q.x * q.y) +
                  tmp_point.y * (q.w * q.w - q.x * q.x + q.y * q.y - q.z * q.z) +
                  tmp_point.z * 2 * (q.y * q.z - q.w * q.x) + center_point.y;
    res_point.z = tmp_point.x * 2 * (q.x * q.z - q.w * q.y) + tmp_point.y * 2 * (q.w * q.x + q.y * q.z) +
                  tmp_point.z * (q.w * q.w - q.x * q.x - q.y * q.y + q.z * q.z) + center_point.z;
}