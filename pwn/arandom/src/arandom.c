#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/random.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/miscdevice.h>

#define DEVICE_NAME "arandom"
#define ALLOCATE_CMD 0x1001
#define FREE_CMD 0x1002
#define WRITE_CMD 0x1003
#define GET_INFO 0x1004
#define GUESS_NUM 0x1005

typedef struct arandom_params {
    u32 rand_size;
    u32 rand_offset;
    u32 rand_value;
}random_info;


static void *buffer = NULL;
random_info AAA;
static bool allocated = false;
static bool freed = false;
static bool writen = false;
static DEFINE_MUTEX(arandom_mutex);

static long arandom_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
    int ret = 0;

    mutex_lock(&arandom_mutex);

    switch (cmd) {
    case ALLOCATE_CMD:
        if (!allocated) {
            buffer = kmalloc(AAA.rand_size, GFP_KERNEL);
            if (!buffer) {
                ret = -ENOMEM;
                goto out;
            }
            allocated = true;
            // printk(KERN_INFO "arandom: Allocated %u bytes\n", rand_size);
        } else {
            ret = -EPERM;
        }
        break;

    case FREE_CMD:
        if (allocated && !freed) {
            kfree(buffer);
            // buffer = NULL;
            freed = true;
            // printk(KERN_INFO "arandom: Buffer freed\n");
        } else {
            ret = -EPERM;
        }
        break;

    case WRITE_CMD:
        if (allocated && !writen) {
            if (AAA.rand_offset + sizeof(int) > AAA.rand_size) {
                ret = -EINVAL;
                goto out;
            }
            *(int *)(buffer + AAA.rand_offset) = AAA.rand_value;
            // printk(KERN_INFO "arandom: Wrote value 0x%x at offset %u\n", 
                //    rand_value, rand_offset);
        } else {
            ret = -EPERM;
        }
        break;

    case GET_INFO:
          if (copy_to_user((void __user *)arg, &AAA, sizeof(AAA))) {
            ret = -EFAULT;
        }
        break;

    case GUESS_NUM:
          if(*(unsigned long long*)(buffer+AAA.rand_offset) == AAA.rand_value && *(unsigned long long*)(buffer+AAA.rand_offset+0x10) == AAA.rand_offset && *(unsigned long long*)(buffer+AAA.rand_offset+0x18) == AAA.rand_size)
            *(unsigned long long*)(buffer+AAA.rand_offset+0x20) = (unsigned long long)&get_random_bytes;
        break;

    default:
        ret = -ENOTTY;
        break;
    }

out:
    mutex_unlock(&arandom_mutex);
    return ret;
}

static int arandom_open(struct inode *inode, struct file *file)
{
    printk(KERN_INFO "AAA has designed a random number generator\n");
    return 0;
}   

static int arandom_release(struct inode *inode, struct file *file)
{
    printk(KERN_INFO "Bye\n");
    return 0;
}   

static struct file_operations arandom_fops = {
    .owner          = THIS_MODULE,
    .unlocked_ioctl = arandom_ioctl,
    .open           = arandom_open,
    .release = arandom_release,
};

static struct miscdevice arandom_miscdev = {
    .minor = MISC_DYNAMIC_MINOR,
    .name  = "arandom",
    .fops  = &arandom_fops,
};


static int __init arandom_init(void)
{
    get_random_bytes(&AAA.rand_size, sizeof(AAA.rand_size));
    AAA.rand_size %= 0x8000;
    if (AAA.rand_size == 0) AAA.rand_size = 0x8000;

    get_random_bytes(&AAA.rand_offset, sizeof(AAA.rand_offset));
    AAA.rand_offset %= (AAA.rand_size - sizeof(int));

    get_random_bytes(&AAA.rand_value, sizeof(AAA.rand_value));

    misc_register(&arandom_miscdev);
    // printk(KERN_INFO "arandom: Module loaded (size=%u, offset=%u, value=0x%x)\n",
        //    rand_size, rand_offset, rand_value);
    return 0;
}

static void __exit arandom_exit(void)
{
    misc_deregister(&arandom_miscdev);
    // printk(KERN_INFO "arandom: Module unloaded\n");
}

module_init(arandom_init);
module_exit(arandom_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Lotus");
MODULE_DESCRIPTION("arandom kernel module");
