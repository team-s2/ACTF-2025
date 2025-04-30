# deeptx

A cuda reverse challenge, this program reads a bmp and uses cuda to "encrypt" the picture. You can cuobjdump it to reverse the cuda part.

```plaintext
Fatbin elf code:
================
arch = sm_86
code version = [1,7]
host = linux
compile_size = 64bit

Fatbin elf code:
================
arch = sm_86
code version = [1,7]
host = linux
compile_size = 64bit

Fatbin ptx code:
================
arch = sm_86
code version = [8,7]
host = linux
compile_size = 64bit
compressed
ptxasOptions = 

//
//
//
//
//
//

.version 8.7
.target sm_86
.address_size 64

//
.const .align 1 .b8 cuda_sbox[256];
.const .align 1 .b8 cuda_tbox[256];
.const .align 4 .b8 cuda_motion[1024];

.visible .entry _Z6Layer1PhS_(
.param .u64 _Z6Layer1PhS__param_0,
.param .u64 _Z6Layer1PhS__param_1
)
{
.reg .pred %p<6>;
.reg .b16 %rs<2>;
.reg .f32 %f<12>;
.reg .b32 %r<23>;
.reg .b64 %rd<15>;


ld.param.u64 %rd5, [_Z6Layer1PhS__param_0];
ld.param.u64 %rd6, [_Z6Layer1PhS__param_1];
mov.u32 %r1, %tid.x;
setp.lt.u32 %p1, %r1, 241;
mov.u32 %r2, %ctaid.x;
setp.lt.u32 %p2, %r2, 241;
and.pred %p3, %p1, %p2;
@%p3 bra $L__BB0_2;
bra.uni $L__BB0_1;

$L__BB0_2:
mov.u32 %r3, %ntid.x;
cvta.to.global.u64 %rd1, %rd5;
mov.f32 %f10, 0f00000000;
mov.u32 %r11, 0;
mov.u64 %rd8, cuda_motion;
mov.u32 %r20, %r11;

$L__BB0_3:
.pragma "nounroll";
add.s32 %r13, %r20, %r2;
shl.b32 %r14, %r20, 4;
mov.u32 %r15, 240;
sub.s32 %r16, %r15, %r14;
mad.lo.s32 %r21, %r13, %r3, %r1;
mul.wide.u32 %rd7, %r16, 4;
add.s64 %rd14, %rd8, %rd7;
mov.u32 %r22, %r11;

$L__BB0_4:
.pragma "nounroll";
cvt.u64.u32 %rd9, %r21;
add.s64 %rd10, %rd1, %rd9;
ld.global.u8 %rs1, [%rd10];
cvt.rn.f32.u16 %f7, %rs1;
ld.const.f32 %f8, [%rd14];
fma.rn.f32 %f10, %f8, %f7, %f10;
add.s32 %r21, %r21, 1;
add.s64 %rd14, %rd14, 4;
add.s32 %r22, %r22, 1;
setp.ne.s32 %p4, %r22, 16;
@%p4 bra $L__BB0_4;

add.s32 %r20, %r20, 1;
setp.lt.u32 %p5, %r20, 16;
@%p5 bra $L__BB0_3;
bra.uni $L__BB0_6;

$L__BB0_1:
mov.f32 %f10, 0f00000000;

$L__BB0_6:
cvt.rzi.u32.f32 %r17, %f10;
mov.u32 %r18, %ntid.x;
mad.lo.s32 %r19, %r2, %r18, %r1;
cvt.u64.u32 %rd11, %r19;
cvta.to.global.u64 %rd12, %rd6;
add.s64 %rd13, %rd12, %rd11;
st.global.u8 [%rd13], %r17;
ret;

}
//
.visible .entry _Z6Layer2PhS_(
.param .u64 _Z6Layer2PhS__param_0,
.param .u64 _Z6Layer2PhS__param_1
)
{
.reg .b16 %rs<2>;
.reg .b32 %r<8>;
.reg .b64 %rd<14>;


ld.param.u64 %rd1, [_Z6Layer2PhS__param_0];
ld.param.u64 %rd2, [_Z6Layer2PhS__param_1];
cvta.to.global.u64 %rd3, %rd2;
cvta.to.global.u64 %rd4, %rd1;
mov.u32 %r1, %ctaid.x;
mov.u32 %r2, %ntid.x;
mov.u32 %r3, %tid.x;
mad.lo.s32 %r4, %r1, %r2, %r3;
cvt.u64.u32 %rd5, %r4;
add.s64 %rd6, %rd4, %rd5;
ld.global.u8 %rs1, [%rd6];
cvt.u64.u32 %rd7, %r3;
mov.u64 %rd8, cuda_sbox;
add.s64 %rd9, %rd8, %rd7;
ld.const.u8 %r5, [%rd9];
cvt.u64.u32 %rd10, %r1;
add.s64 %rd11, %rd8, %rd10;
ld.const.u8 %r6, [%rd11];
mad.lo.s32 %r7, %r2, %r5, %r6;
cvt.u64.u32 %rd12, %r7;
add.s64 %rd13, %rd3, %rd12;
st.global.u8 [%rd13], %rs1;
ret;

}
//
.visible .entry _Z6Layer3PhS_(
.param .u64 _Z6Layer3PhS__param_0,
.param .u64 _Z6Layer3PhS__param_1
)
{
.reg .pred %p<5>;
.reg .b16 %rs<33>;
.reg .b32 %r<52>;
.reg .b64 %rd<24>;


ld.param.u64 %rd6, [_Z6Layer3PhS__param_0];
ld.param.u64 %rd5, [_Z6Layer3PhS__param_1];
mov.u32 %r21, %ntid.x;
mov.u32 %r1, %ctaid.x;
mul.lo.s32 %r49, %r1, %r21;
mov.u32 %r3, %tid.x;
add.s32 %r22, %r49, %r3;
cvt.u64.u32 %rd1, %r22;
cvta.to.global.u64 %rd2, %rd6;
add.s64 %rd3, %rd2, %rd1;
cvt.u16.u32 %rs8, %r3;
cvt.u16.u32 %rs9, %r1;
or.b16 %rs10, %rs9, %rs8;
ld.global.u8 %rs11, [%rd3];
xor.b16 %rs12, %rs11, %rs10;
st.global.u8 [%rd3], %rs12;
bar.sync 0;
and.b32 %r23, %r3, 7;
setp.ne.s32 %p1, %r23, 0;
@%p1 bra $L__BB2_4;

ld.global.u32 %r47, [%rd3+4];
ld.global.u32 %r48, [%rd3];
mov.u32 %r46, 1786956040;
mov.u32 %r45, 0;

$L__BB2_2:
.pragma "nounroll";
shl.b32 %r26, %r48, 4;
add.s32 %r27, %r26, 1386807340;
shr.u32 %r28, %r48, 5;
add.s32 %r29, %r28, 2007053320;
xor.b32 %r30, %r29, %r27;
add.s32 %r31, %r48, %r46;
xor.b32 %r32, %r30, %r31;
add.s32 %r47, %r32, %r47;
shl.b32 %r33, %r47, 4;
add.s32 %r34, %r33, 621668851;
add.s32 %r35, %r46, %r47;
xor.b32 %r36, %r34, %r35;
shr.u32 %r37, %r47, 5;
add.s32 %r38, %r37, -862448841;
xor.b32 %r39, %r36, %r38;
sub.s32 %r48, %r48, %r39;
add.s32 %r46, %r46, -1708609273;
add.s32 %r45, %r45, 1;
setp.ne.s32 %p2, %r45, 3238567;
@%p2 bra $L__BB2_2;

st.global.u32 [%rd3], %r48;
st.global.u32 [%rd3+4], %r47;

$L__BB2_4:
bar.sync 0;
and.b16 %rs16, %rs9, %rs8;
ld.global.u8 %rs17, [%rd3];
xor.b16 %rs18, %rs17, %rs16;
st.global.u8 [%rd3], %rs18;
bar.sync 0;
cvt.u64.u32 %rd7, %r3;
mov.u64 %rd8, cuda_sbox;
add.s64 %rd9, %rd8, %rd7;
ld.const.u8 %rs31, [%rd9];
cvta.to.global.u64 %rd4, %rd5;
mov.u16 %rs32, 0;
mov.u32 %r50, 0;
mov.u64 %rd14, cuda_tbox;

$L__BB2_5:
.pragma "nounroll";
cvt.u64.u32 %rd10, %r49;
add.s64 %rd11, %rd2, %rd10;
cvt.u64.u16 %rd12, %rs31;
and.b64 %rd13, %rd12, 255;
add.s64 %rd15, %rd14, %rd13;
ld.const.u8 %rs19, [%rd15];
ld.global.u8 %rs20, [%rd11];
mul.lo.s16 %rs21, %rs19, %rs20;
add.s16 %rs32, %rs21, %rs32;
mul.lo.s16 %rs22, %rs31, 5;
add.s16 %rs31, %rs22, 17;
add.s32 %r49, %r49, 1;
add.s32 %r50, %r50, 1;
setp.ne.s32 %p3, %r50, 256;
@%p3 bra $L__BB2_5;

xor.b32 %r18, %r1, %r3;
mov.u32 %r51, 8;

$L__BB2_7:
.pragma "nounroll";
shl.b16 %rs23, %rs32, 3;
and.b16 %rs24, %rs32, 224;
shr.u16 %rs25, %rs24, 5;
or.b16 %rs26, %rs25, %rs23;
cvt.u32.u16 %r42, %rs26;
mad.lo.s32 %r43, %r42, 13, %r18;
and.b32 %r44, %r51, 255;
cvt.u64.u32 %rd16, %r44;
add.s64 %rd18, %rd14, %rd16;
cvt.u16.u32 %rs27, %r43;
ld.const.u8 %rs28, [%rd18];
xor.b16 %rs29, %rs28, %rs27;
cvt.u64.u16 %rd19, %rs29;
and.b64 %rd20, %rd19, 255;
add.s64 %rd22, %rd8, %rd20;
ld.const.u8 %rs32, [%rd22];
add.s32 %r51, %r51, 1;
setp.ne.s32 %p4, %r51, 4137823;
@%p4 bra $L__BB2_7;

add.s64 %rd23, %rd4, %rd1;
st.global.u8 [%rd23], %rs32;
ret;

}
```

I add the nounroll pragma to decrease the difficulty.

Layer1 is a conv-like code, and the variable name "cuda_motion" indicates that this may be a motion blur code. You can ask LLM how to deblur it, it may give you code of Inverse Filtering or Wiener Filtering.

Layer2 is just a sbox operation, you can easily reverse it.

Layer3 is somewhat bloated, you need to carefully reverse it, it includes TEA encryption, matrix multiplication, and some other operations. You can reverse it step by step, and you should use sagemath or other tools to calculate the inverse matrix.

Here is the sample solve script (no deblur part):

```cpp
#include <iostream>
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <cstdlib>
#include <fstream>
#include <cuda_runtime.h>

__constant__ uint8_t cuda_sbox[256];
__constant__ uint8_t cuda_sbox_rev[256];
__constant__ uint8_t cuda_tbox[256];

const uint8_t sbox[256] = {...};

const uint8_t sbox_rev[256] = {...};

const uint8_t tbox[256] = {...};

uint8_t matrix[65536] = {...};

__global__ void RevLayer3(uint8_t *input, uint8_t *output, uint8_t *matrix)
{
    uint32_t block_id = blockIdx.x;
    uint32_t block_dim = blockDim.x;
    uint32_t thread_id = threadIdx.x;
    uint32_t index = blockIdx.x * blockDim.x + threadIdx.x;

    uint8_t ch = input[index];

    for (uint32_t i = 0x3f235e; i >= 8; i--)
    {
        ch = cuda_sbox_rev[ch];
        ch ^= cuda_tbox[i % 256];
        ch -= block_id ^ thread_id;
        ch = 197 * ch;
        ch = (ch << 5) | (ch >> 3);
    }

    input[index] = ch;

    __syncthreads();

    ch = 0;

    for (uint32_t i = 0; i < 256; i++)
    {
        ch += input[block_id * block_dim + i] * matrix[thread_id * block_dim + i];
    }

    ch ^= block_id & thread_id;

    output[index] = ch;

    __syncthreads();

    if (thread_id % 8 == 0)
    {
        uint32_t v0 = *(uint32_t *)(output + index);
        uint32_t v1 = *(uint32_t *)(output + index + 4);

        uint32_t sum = 0xb6b22a99;

        for (uint32_t i = 0; i < 0x316aa7; i++)
        {
            sum -= 0x9a28b107;
            v0 += ((v1 << 4) + 0x250de9f3) ^ (v1 + sum) ^ ((v1 >> 5) + 0xcc981337);
            v1 -= ((v0 << 4) + 0x52a9002c) ^ (v0 + sum) ^ ((v0 >> 5) + 0x77a13408);
        }
        *(uint32_t *)(output + index) = v0;
        *(uint32_t *)(output + index + 4) = v1;
    }

    __syncthreads();

    output[index] ^= block_id | thread_id;
}

__global__ void RevLayer2(uint8_t *input, uint8_t *output)
{
    output[cuda_sbox_rev[threadIdx.x] * blockDim.x + cuda_sbox_rev[blockIdx.x]] = input[blockIdx.x * blockDim.x + threadIdx.x];
}

__global__ void TempLayer(uint8_t *input, uint8_t *output)
{
    output[blockIdx.x * blockDim.x + threadIdx.x] = input[blockIdx.x * blockDim.x + threadIdx.x];
}

#pragma pack(push, 1)
struct BMPFileHeader
{
    uint16_t bfType;
    uint32_t bfSize;
    uint16_t bfReserved1;
    uint16_t bfReserved2;
    uint32_t bfOffBits;
};

struct BMPInfoHeader
{
    uint32_t biSize;
    int32_t biWidth;
    int32_t biHeight;
    uint16_t biPlanes;
    uint16_t biBitCount;
    uint32_t biCompression;
    uint32_t biSizeImage;
    int32_t biXPelsPerMeter;
    int32_t biYPelsPerMeter;
    uint32_t biClrUsed;
    uint32_t biClrImportant;
};
#pragma pack(pop)

int main()
{
    std::ifstream input_file("deep_flag.bmp", std::ios::binary);

    if (!input_file)
        return -1;

    BMPFileHeader file_header;

    input_file.read(reinterpret_cast<char *>(&file_header), sizeof(file_header));

    BMPInfoHeader info_header;
    input_file.read(reinterpret_cast<char *>(&info_header), sizeof(info_header));

    if (info_header.biWidth != 0x100)
        return -1;
    if (info_header.biHeight != 0x100)
        return -1;

    if (info_header.biBitCount != 8)
        return -1;
    if (info_header.biCompression != 0)
        return -1;

    uint32_t colors[256];
    input_file.read(reinterpret_cast<char *>(colors), sizeof(colors));

    uint8_t *input = static_cast<uint8_t *>(malloc(65536));
    uint8_t *output = static_cast<uint8_t *>(malloc(65536));

    uint8_t *cuda_input, *cuda_output;
    uint8_t *cuda_matrix;
    cudaMemcpyToSymbol(cuda_sbox, sbox, 256);
    cudaMemcpyToSymbol(cuda_tbox, tbox, 256);
    cudaMemcpyToSymbol(cuda_sbox_rev, sbox_rev, 256);
    cudaMalloc(&cuda_input, 65536);
    cudaMalloc(&cuda_output, 65536);

    cudaMalloc(&cuda_matrix, 65536);
    cudaMemcpy(cuda_matrix, matrix, 65536, cudaMemcpyHostToDevice);

    input_file.read(reinterpret_cast<char *>(input), 65536);
    input_file.close();
    cudaMemcpy(cuda_input, input, 65536, cudaMemcpyHostToDevice);
    RevLayer3<<<256, 256>>>(cuda_input, cuda_output, cuda_matrix);
    cudaDeviceSynchronize();
    RevLayer2<<<256, 256>>>(cuda_output, cuda_input);
    cudaDeviceSynchronize();
    TempLayer<<<256, 256>>>(cuda_input, cuda_output);
    cudaDeviceSynchronize();
    cudaMemcpy(output, cuda_output, 65536, cudaMemcpyDeviceToHost);
    std::ofstream output_file("dec_flag.bmp", std::ios::binary);

    output_file.write(reinterpret_cast<const char *>(&file_header), sizeof(file_header));
    output_file.write(reinterpret_cast<const char *>(&info_header), sizeof(info_header));
    output_file.write(reinterpret_cast<const char *>(colors), sizeof(colors));
    output_file.write(reinterpret_cast<const char *>(output), 65536);
    output_file.close();

    free(input);
    free(output);
    cudaFree(cuda_input);
    cudaFree(cuda_output);
}
```