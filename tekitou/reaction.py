import numpy as np
import matplotlib.pyplot as plt

# モーターとホイールのパラメータ
R = 1.0          # モーターの抵抗 (ohm)
L = 0.5          # モーターのインダクタンス (H)
k_e = 0.1        # 逆起電力定数 (V/(rad/s))
k_t = 0.1        # トルク定数 (Nm/A)
I_w = 0.1       # ホイールの慣性モーメント (kg*m^2)
I_s = 10.0        # システムの慣性モーメント (kg*m^2)
dt = 0.01        # タイムステップ (秒)
t_max = 5.0      # シミュレーション時間 (秒)

# モーターにかける電圧
V_motor = 5.0

# 初期状態
theta_s = 0.0     # システムの角度 (ラジアン)
omega_s = 0.0     # システムの角速度 (rad/s)
omega_w = 0.0     # ホイールの角速度 (rad/s)
i_motor = 0.0     # モーターの電流 (A)

# 時間の配列
time = np.arange(0, t_max, dt)

# 結果を保存するリスト
theta_s_history = []
omega_s_history = []
omega_w_history = []
i_motor_history = []

# シミュレーションループ
for t in time:
    # モーターの電気方程式から電流の変化を計算
    di_dt = (V_motor - R * i_motor - k_e * omega_w) / L
    i_motor += di_dt * dt

    # モーターのトルクを計算
    tau_motor = k_t * i_motor

    # ホイールの角加速度の計算
    alpha_w = tau_motor / I_w
    omega_w += alpha_w * dt

    # システムへの反トルクによる角加速度
    alpha_s = - (I_w * alpha_w) / I_s
    omega_s += alpha_s * dt

    # システムの角度の更新
    theta_s += omega_s * dt

    # データを保存
    theta_s_history.append(theta_s)
    omega_s_history.append(omega_s)
    omega_w_history.append(omega_w)
    i_motor_history.append(i_motor)

# 結果のプロット
plt.figure(figsize=(10, 8))

# システムの角度
plt.subplot(4, 1, 1)
plt.plot(time, theta_s_history, label='System Angle (theta_s)')
plt.xlabel('Time (s)')
plt.ylabel('Angle (rad)')
plt.grid(True)
plt.legend()

# システムの角速度
plt.subplot(4, 1, 2)
plt.plot(time, omega_s_history, label='System Angular Velocity (omega_s)', color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Angular Velocity (rad/s)')
plt.grid(True)
plt.legend()

# ホイールの角速度
plt.subplot(4, 1, 3)
plt.plot(time, omega_w_history, label='Wheel Angular Velocity (omega_w)', color='green')
plt.xlabel('Time (s)')
plt.ylabel('Angular Velocity (rad/s)')
plt.grid(True)
plt.legend()

# モーターの電流
plt.subplot(4, 1, 4)
plt.plot(time, i_motor_history, label='Motor Current (i_motor)', color='red')
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
