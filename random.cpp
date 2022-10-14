#include <bits/stdc++.h>

#define P_MIN -12.5f
#define P_MAX 12.5f
#define V_MIN -8.0f
#define V_MAX 8.0f
#define KP_MIN 0.0f
#define KP_MAX 500.0f
#define KD_MIN 0.0f
#define KD_MAX 5.0f
#define T_MIN -144.0f
#define T_MAX 144.0f

using namespace std;

int main(){

    int p_int = 65535, v_int = 2047, kp_int = 819, kd_int = 4095, t_int =2474;

    vector<int> buf(8);
    buf[0] = p_int >> 8;
    buf[1] = p_int & 0xFF;
    buf[2] = v_int >> 4;
    buf[3] = ((v_int & 0xF) << 4) | (kp_int >> 8);
    buf[4] = kp_int & 0xFF;
    buf[5] = kd_int >> 4;
    buf[6] = ((kd_int & 0xF) << 4) | (t_int >> 8);
    buf[7] = t_int & 0xFF;

    for (auto i: buf) cout <<hex << i << ' ';

    return 0;
}