#include <Wire.h>
#include <math.h>

// MPU6050 I2C Address
const int MPU6050_ADDR = 0x68;

// MPU6050 Registers
const int PWR_MGMT_1 = 0x6B;
const int ACCEL_XOUT_H = 0x3B;

// Gravity constant for conversion
const float ACCEL_SCALE = 16384.0; // Assuming +/-2g setting



void setupMPU6050() {
    Wire.begin();
    Wire.beginTransmission(MPU6050_ADDR);
    Wire.write(PWR_MGMT_1);  // Select power management register
    Wire.write(0);  // Wake up MPU6050 (clear sleep mode)
    Wire.endTransmission(true);
    Serial.println("MPU6050 initialized.");
}

void readMPU6050() {
    Wire.beginTransmission(MPU6050_ADDR);
    Wire.write(ACCEL_XOUT_H); // Start reading from ACCEL_XOUT_H register
    Wire.endTransmission(false);
    Wire.requestFrom(MPU6050_ADDR, 6, true); // Request 6 bytes (accelX, accelY, accelZ)

    // Read accelerometer values
    accelX = (Wire.read() << 8) | Wire.read();
    accelY = (Wire.read() << 8) | Wire.read();
    accelZ = (Wire.read() << 8) | Wire.read();
    
    // Convert to g-force
    float Ax = accelX / ACCEL_SCALE;
    float Ay = accelY / ACCEL_SCALE;
    float Az = accelZ / ACCEL_SCALE;

    // Calculate angles
    anglePitch = atan2(Ax, sqrt(Ay * Ay + Az * Az)) * (180.0 / M_PI);
    angleRoll = atan2(Ay, sqrt(Ax * Ax + Az * Az)) * (180.0 / M_PI);

   
}


