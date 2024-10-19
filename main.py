import numpy as np


def _regularize_4sq(arr: np.ndarray) -> np.ndarray:
    if len(arr) < 4:
        return arr
    arr[3, 0:3] = 0
    arr[3, 3] = 1
    return arr


def _regularize_4rec(arr: np.ndarray) -> np.ndarray:
    if len(arr) < 4:
        return arr
    arr[3] = 1
    return arr


def gen_random_c_arr(size: int) -> np.ndarray:
    random_c = np.random.randint(0, 255, (4, size), dtype=np.uint8)
    return _regularize_4rec(random_c)


def gen_turbulence_mat(amp: float) -> np.ndarray:
    turbulence_mat = np.eye(4) + (np.random.random((4, 4)) - 0.5) * amp
    return _regularize_4sq(turbulence_mat).astype(np.float32)


def turbulence(arr: np.ndarray, turb_arr: np.ndarray, second_turb_amp: float = 0.01) -> np.ndarray:
    ret = turb_arr @ arr
    rand = second_turb_amp * (np.random.random(ret.shape).astype(np.float32) - 0.5)
    return _regularize_4rec(ret + rand)


def clip(arr: np.ndarray) -> np.ndarray:
    arr[arr < 0] = 0
    arr[arr > 255] = 255
    return np.round(arr).astype(np.uint8)


if __name__ == "__main__":
    c_origin = gen_random_c_arr(10)
    a = gen_turbulence_mat(0.1)

    # C_obs = A * C_origin
    c_obs = turbulence(c_origin, a, second_turb_amp=0.01)

    # C_origin^-1 = pinv(c_origin)
    pinv = np.linalg.pinv(c_origin.astype(np.float32))

    # A_hat = c_obs * C_origin^-1
    a_hat = c_obs.astype(np.float32) @ pinv

    # C_reconst = A_hat * C_origin
    c_reconst = clip(np.linalg.inv(a_hat) @ c_obs)

    print("C original")
    print(c_origin)
    print("A")
    print(a)
    print("C obs")
    print(clip(c_obs))
    print("A_hat")
    print(a_hat)
    print("|A - A_hat|")
    print(np.abs(a - a_hat))
    print("C reconst")
    print(clip(c_reconst))
    print("obs - reconst")
    print(c_origin.astype(np.int32) - c_reconst.astype(np.int32))
