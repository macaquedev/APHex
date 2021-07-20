#include <Python.h>
#include <math.h>
#include <stdio.h>

#define PI 3.141592653589793
#define PI_OVER_TWO 1.5707963267948966
#define RADIAN_CONSTANT 0.017453292519943295

typedef struct {
    double rho, phi;
} Polar;

typedef struct {
    double x, y;
} Cartesian2D;

typedef struct {
    double x, y, z;
} Cartesian3D;

typedef struct {
    double x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, x5, y5, z5, x6, y6, z6;
} Cartesian6;

typedef struct {
    int tibia, femur, coxa;
} LegServos;

typedef struct {
    double tibia, femur, coxa;
} LegServoSpeeds;

typedef struct { 
    int tibia_num, femur_num, coxa_num;
    int tibia_angle, femur_angle, coxa_angle;
    double tibia_speed, femur_speed, coxa_speed;
} ServoSpeeds;

Polar cartesianToPolar(Cartesian2D *coords) {
    Polar out;
    out.rho = sqrt((coords->x * coords->x) + (coords->y * coords->y));
    out.phi = atan2(coords->y, coords->x) / RADIAN_CONSTANT;
    return out;
}

Cartesian2D polarToCartesian(Polar *coords) {
    Cartesian2D out;
    double phi = coords->phi * RADIAN_CONSTANT;
    out.x = coords->rho * cos(phi);
    out.y = coords->rho * sin(phi);
    return out;
}

LegServos cartesianToServo(int leg, Cartesian3D *coords, double foot_length, double leg_length, double hip_length) {
    double x = coords->x;
    double y = coords->y;
    double z = coords->z;
    z -= (foot_length - 90);
    double w = (x >= 0 ? 1 : -1) * sqrt((x * x) + (y * y));
    double v = w - hip_length;

    float a = atan2(z, v) + acos(((leg_length * leg_length) - (foot_length * foot_length) + (v * v) + (z * z)) / 2 / leg_length / sqrt((v * v) + (z * z)));
    float b = acos(((leg_length * leg_length) + (foot_length * foot_length) - (v * v) - (z * z)) / 2 / leg_length / foot_length);
    float g = (w >= 0) ? atan2(y, x) : atan2(-y, -x);
    
    int alpha = a / RADIAN_CONSTANT;
    int beta = b / RADIAN_CONSTANT;
    int gamma = g / RADIAN_CONSTANT;

    switch(leg) {
        case 0:
            alpha = 135 - alpha;
            beta += 25;
            gamma = 150 - gamma;
            break;
        case 1:
            alpha += 45;
            beta = 155 - beta;
            gamma += 30;
            break;
        case 2:
            alpha = 135 - alpha;
            beta += 25;
            gamma = 90 - gamma;
            break;
        case 3:
            alpha += 45;
            beta = 155 - beta;
            gamma += 90;
            break;
        case 4:
            alpha = 135 - alpha;
            beta += 25;
            gamma += 30;
            break;
        case 5:
            alpha += 45;
            beta = 155 - beta;
            gamma = 150 - gamma;
            break;
    }

    LegServos out = {beta, alpha, gamma};
    return out;
}

ServoSpeeds speedCalc(int leg, Cartesian3D *coords, double speed, double foot_length, double leg_length, double hip_length, int  *current_positions) {
    speed = pow(7.5 - (speed / 15), 2);
    LegServos angles = cartesianToServo(leg, coords, foot_length, leg_length, hip_length);
    int c_tibia = current_positions[leg*3];
    int c_femur = current_positions[leg*3+1];
    int c_coxa = current_positions[leg*3+2];
    int differences[3] = { angles.tibia - c_tibia, angles.femur - c_femur, angles.coxa - c_coxa };
    int max_diff = 0;
    for (int i = 0; i < 3; i++) {
        if (abs(differences[i]) > max_diff) 
            max_diff = abs(differences[i]);
    }
    double tibia_speed, femur_speed, coxa_speed;
    if (differences[0] != 0) { tibia_speed = abs(1.0 / (double)differences[0] * (double)max_diff * (double)speed); }
    else { tibia_speed = 0; }
    if (differences[1] != 0) { femur_speed = abs(1.0 / (double)differences[1] * (double)max_diff * (double)speed); }
    else { femur_speed = 0; }
    if (differences[2] != 0) { coxa_speed = abs(1.0 / (double)differences[2] * (double)max_diff * (double)speed); }
    else { coxa_speed = 0; }

    LegServos nums = { leg * 3, leg * 3 + 1, leg * 3 + 2 };
    LegServoSpeeds speeds = { tibia_speed, femur_speed, coxa_speed };
    ServoSpeeds out;
    out.tibia_num = nums.tibia;
    out.femur_num = nums.femur;
    out.coxa_num = nums.coxa;
    out.tibia_angle = angles.tibia;
    out.femur_angle = angles.femur;
    out.coxa_angle = angles.coxa;
    out.tibia_speed = speeds.tibia;
    out.femur_speed = speeds.femur;
    out.coxa_speed = speeds.coxa;
    return out;
}

Cartesian6 shiftLean(double posX, double posY, double posZ, double rotX, double rotY, double rotZ, double bodySideLength, double tibiaLength, double femurLength, double coxaLength) {
    posX *= -1;
    posY *= -1;
    posZ *= -1;
    double temp = rotY;
    rotY = rotZ;
    rotZ = temp;
    
    double bco1 = bodySideLength / 2;
    double bco2 = sqrt((bodySideLength * bodySideLength) - (bco1 * bco1));

    double bcox1 = bco1;
    double bcox2 = bodySideLength;
    double bcox3 = bco1;
    double bcox4 = -bco1;
    double bcox5 = -bodySideLength;
    double bcox6 = -bco1;

    double bcoy1 = bco2;
    double bcoy2 = 0;
    double bcoy3 = -bco2;
    double bcoy4 = -bco2;
    double bcoy5 = 0;
    double bcoy6 = bco2;

    double fpx1 = 0.5 * (coxaLength + femurLength);
    double fpy1 = 0.866025404 * (coxaLength + femurLength);

    double fpx2 = coxaLength + femurLength;
    double fpy2 = 0;

    double fpx3 = 0.5 * (coxaLength + femurLength);
    double fpy3 = -0.866025404 * (coxaLength + femurLength);

    double fpx4 = -0.5 * (coxaLength + femurLength);
    double fpy4 = -0.866025404 * (coxaLength + femurLength);

    double fpx5 = -coxaLength - femurLength;
    double fpy5 = 0;

    double fpx6 = -0.5 * (coxaLength + femurLength);
    double fpy6 = 0.866025404 * (coxaLength + femurLength);

    double ty1 = fpy1 + bcoy1 + posY;
    double tx1 = fpx1 + bcox1 + posX;
    double dbcf1 = sqrt((ty1 * ty1) + (tx1 * tx1));
    double abcx1 = PI_OVER_TWO - atan2(tx1, ty1);
    double rz1 = tan(rotZ * RADIAN_CONSTANT) * tx1;
    double pz1 = tan(rotX * RADIAN_CONSTANT) * ty1;
    double bikx1 = cos(abcx1 + (rotY * RADIAN_CONSTANT)) * dbcf1 - tx1;
    double biky1 = (sin(abcx1 + (rotY * RADIAN_CONSTANT)) * dbcf1) - ty1;
    double bikz1 = rz1 + pz1;
    double npx1 = fpx1 + posX + bikx1;
    double npy1 = fpy1 + posY + biky1;
    double npz1 = posZ + bikz1;

    double ty2 = fpy2 + bcoy2 + posY;
    double tx2 = fpx2 + bcox2 + posX;
    double dbcf2 = sqrt((ty2 * ty2) + (tx2 * tx2));
    double abcx2 = PI_OVER_TWO - atan2(tx2, ty2);
    double rz2 = tan(rotZ * RADIAN_CONSTANT) * tx2;
    double pz2 = tan(rotX * RADIAN_CONSTANT) * ty2;
    double bikx2 = cos(abcx2 + (rotY * RADIAN_CONSTANT)) * dbcf2 - tx2;
    double biky2 = (sin(abcx2 + (rotY * RADIAN_CONSTANT)) * dbcf2) - ty2;
    double bikz2 = rz2 + pz2;
    double npx2 = fpx2 + posX + bikx2;
    double npy2 = fpy2 + posY + biky2;
    double npz2 = posZ + bikz2;

    double ty3 = fpy3 + bcoy3 + posY;
    double tx3 = fpx3 + bcox3 + posX;
    double dbcf3 = sqrt((ty3 * ty3) + (tx3 * tx3));
    double abcx3 = PI_OVER_TWO - atan2(tx3, ty3);
    double rz3 = tan(rotZ * RADIAN_CONSTANT) * tx3;
    double pz3 = tan(rotX * RADIAN_CONSTANT) * ty3;
    double bikx3 = cos(abcx3 + (rotY * RADIAN_CONSTANT)) * dbcf3 - tx3;
    double biky3 = (sin(abcx3 + (rotY * RADIAN_CONSTANT)) * dbcf3) - ty3;
    double bikz3 = rz3 + pz3;
    double npx3 = fpx3 + posX + bikx3;
    double npy3 = -fpy3 - posY - biky3;
    double npz3 = posZ + bikz3;

    double ty4 = fpy4 + bcoy4 + posY;
    double tx4 = fpx4 + bcox4 + posX;
    double dbcf4 = sqrt((ty4 * ty4) + (tx4 * tx4));
    double abcx4 = PI_OVER_TWO - atan2(tx4, ty4);
    double rz4 = tan(rotZ * RADIAN_CONSTANT) * tx4;
    double pz4 = tan(rotX * RADIAN_CONSTANT) * ty4;
    double bikx4 = cos(abcx4 + (rotY * RADIAN_CONSTANT)) * dbcf4 - tx4;
    double biky4 = (sin(abcx4 + (rotY * RADIAN_CONSTANT)) * dbcf4) - ty4;
    double bikz4 = rz4 + pz4;
    double npx4 = -fpx4 - posX - bikx4;
    double npy4 = -fpy4 - posY - biky4;
    double npz4 = posZ + bikz4;

    double ty5 = fpy5 + bcoy5 + posY;
    double tx5 = fpx5 + bcox5 + posX;
    double dbcf5 = sqrt((ty5 * ty5) + (tx5 * tx5));
    double abcx5 = PI_OVER_TWO - atan2(tx5, ty5);
    double rz5 = tan(rotZ * RADIAN_CONSTANT) * tx5;
    double pz5 = tan(rotX * RADIAN_CONSTANT) * ty5;
    double bikx5 = cos(abcx5 + (rotY * RADIAN_CONSTANT)) * dbcf5 - tx5;
    double biky5 = (sin(abcx5 + (rotY * RADIAN_CONSTANT)) * dbcf5) - ty5;
    double bikz5 = rz5 + pz5;
    double npx5 = -fpx5 - posX - bikx5;
    double npy5 = fpy5 + posY + biky5;
    double npz5 = posZ + bikz5;

    double ty6 = fpy6 + bcoy6 + posY;
    double tx6 = fpx6 + bcox6 + posX;
    double dbcf6 = sqrt((ty6 * ty6) + (tx6 * tx6));
    double abcx6 = PI_OVER_TWO - atan2(tx6, ty6);
    double rz6 = tan(rotZ * RADIAN_CONSTANT) * tx6;
    double pz6 = tan(rotX * RADIAN_CONSTANT) * ty6;
    double bikx6 = cos(abcx6 + (rotY * RADIAN_CONSTANT)) * dbcf6 - tx6;
    double biky6 = (sin(abcx6 + (rotY * RADIAN_CONSTANT)) * dbcf6) - ty6;
    double bikz6 = rz6 + pz6;
    double npx6 = -fpx6 - posX - bikx6;
    double npy6 = fpy6 + posY + biky6;
    double npz6 = posZ + bikz6;

    Cartesian6 out;
    out.x1 = npx1;
    out.y1 = npy1;
    out.z1 = npz1;
    out.x2 = npx2;
    out.y2 = npy2;
    out.z2 = npz2;
    out.x3 = npx3;
    out.y3 = npy3;
    out.z3 = npz3;
    out.x4 = npx4;
    out.y4 = npy4;
    out.z4 = npz4;
    out.x5 = npx5;
    out.y5 = npy5;
    out.z5 = npz5;
    out.x6 = npx6;
    out.y6 = npy6;
    out.z6 = npz6;

    return out;
}

static PyObject* Py_Cartesian2DToPolar(PyObject* self, PyObject* args) {
    double x, y;
    if(!PyArg_ParseTuple(args, "dd", &x, &y)) return NULL;
    Cartesian2D coords = {x, y};
    Polar out = cartesianToPolar(&coords);
    return Py_BuildValue("dd", out.rho, out.phi);
};

static PyObject* Py_PolarToCartesian2D(PyObject* self, PyObject* args) {
    double rho, phi;
    if(!PyArg_ParseTuple(args, "dd", &rho, &phi)) return NULL;
    Polar coords = {rho, phi};
    Cartesian2D out = polarToCartesian(&coords);
    return Py_BuildValue("dd", out.x, out.y);
};

static PyObject* Py_CartesianToServoCalculation(PyObject* self, PyObject* args) {
    double x, y, z, speed, foot_length, leg_length, hip_length;
    int leg;
    PyObject *cp;
    if(!PyArg_ParseTuple(args, "idddddddO", &leg, &x, &y, &z, &speed, &foot_length, &leg_length, &hip_length, &cp)) return NULL;
    int n = PyObject_Length(cp);
    if(n != 18) {
        return NULL;
    }
    int current_positions[n];
    for (int i = 0; i < 18; i++) {
        PyObject *item = PyList_GetItem(cp, i);
        int num = (int)PyLong_AsLong(item);
        current_positions[i] = num;
    }
    Cartesian3D coords = {x, y, z};
    ServoSpeeds out = speedCalc(leg, &coords, speed, foot_length, leg_length, hip_length, &current_positions[0]);
    return Py_BuildValue("[iii][iii][ddd]", out.tibia_num, out.femur_num, out.coxa_num, out.tibia_angle, out.femur_angle, out.coxa_angle, out.tibia_speed, out.femur_speed, out.coxa_speed);
};

static PyObject* Py_ShiftLeanCalculation(PyObject* self, PyObject* args) {
    double posX, posY, posZ, rotX, rotY, rotZ, bodySideLength, tibiaLength, femurLength, coxaLength;
    if(!PyArg_ParseTuple(args, "dddddddddd", &posX, &posY, &posZ, &rotX, &rotY, &rotZ, &bodySideLength, &tibiaLength, &femurLength, &coxaLength)) return NULL;
    Cartesian6 out = shiftLean(posX, posY, posZ, rotX, rotY, rotZ, bodySideLength, tibiaLength, femurLength, coxaLength);
    return Py_BuildValue("[[ddd][ddd][ddd][ddd][ddd][ddd]]",
        out.x6, out.y6, out.z6,
        out.x1, out.y1, out.z1,  
        out.x5, out.y5, out.z5,
        out.x2, out.y2, out.z2,
        out.x4, out.y4, out.z4,
        out.x3, out.y3, out.z3
    );
}

static PyMethodDef ikMethods[] = {
    {"cartesian_to_polar", Py_Cartesian2DToPolar, METH_VARARGS, "Converts cartesian coordinates (x, y) to polar coordinates (rho, phi)"},
    {"polar_to_cartesian", Py_PolarToCartesian2D, METH_VARARGS, "Converts polar coordinates (rho, phi) to cartesian coordinates (x, y)"},
    {"cartesian_to_servo", Py_CartesianToServoCalculation, METH_VARARGS, "Converts cartesian coordinates (x, y, z) for a specific leg to (tibia, femur, coxa)"},
    {"shift_lean", Py_ShiftLeanCalculation, METH_VARARGS, "Takes in 10 arguments (posX, posY, posZ, rotX, rotY, rotZ, bodySideLength, tibiaLength, femurLength, coxaLength) and outputs the resulting servo angles."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef hexIK = {
    PyModuleDef_HEAD_INIT,
    "hex_ik",
    "Module for APHex Inverse Kinematics",
    -1,
    ikMethods
};

PyMODINIT_FUNC PyInit_hex_ik(void) {
    return PyModule_Create(&hexIK);
}
