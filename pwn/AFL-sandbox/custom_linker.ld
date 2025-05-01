/* Thank to LLM */
ENTRY(entry)  /* Specify the entry point of the program */

SECTIONS
{
    . = 0x10000; /* Set the base address for the .text.main section */
    .text.main : { *(.text.main) } /* Place main at 0x10000 */

    . = ALIGN(4); /* Align to the next 4-byte boundary */
    .text : { *(.text) } /* Place all other code sections here */

    . = 0x20000; /* Set the base address for the .data section (global data) */
    .data : { *(.data) } /* Place all global data sections here */

    .bss : { *(.bss) } /* Place uninitialized data sections here */
}