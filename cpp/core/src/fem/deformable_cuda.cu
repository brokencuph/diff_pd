#include "deformable_cuda.h"

#include <cstdlib>
#include <algorithm>
#include <numeric>
#include <iterator>
#include <iostream>

using namespace std;

__global__ void addWithCuda(const int* a, const int* b, int* c)
{
    auto idx = blockIdx.x * blockDim.x + threadIdx.x;
    c[idx] = max(a[idx], b[idx]);
}

void test_add()
{
    const int N = 100;
    int* host_a = new int[N];
    int* host_b = new int[N];
    int* host_c = new int[N];

    iota(host_a, host_a + N, 0);
    iota(host_b, host_b + N, 10);

    int* dev_a;
    int* dev_b;
    int* dev_c;

    cudaMalloc(&dev_a, N * sizeof(int));
    cudaMalloc(&dev_b, N * sizeof(int));
    cudaMalloc(&dev_c, N * sizeof(int));

    cudaMemcpy(dev_a, host_a, N * sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpy(dev_b, host_b, N * sizeof(int), cudaMemcpyHostToDevice);

    addWithCuda<<<N, 1>>>(dev_a, dev_b, dev_c);

    cudaThreadSynchronize();

    cudaMemcpy(host_c, dev_c, N * sizeof(int), cudaMemcpyDeviceToHost);

    copy(host_c, host_c + N, ostream_iterator<int>(cout, " "));
}