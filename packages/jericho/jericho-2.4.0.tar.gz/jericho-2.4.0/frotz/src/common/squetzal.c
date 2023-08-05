/* quetzal.c  - Saving and restoring of Quetzal files.
 *	Written by Martin Frost <mdf@doc.ic.ac.uk>
 *
 * This file is part of Frotz.
 *
 * Frotz is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Frotz is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 */

#include <stdio.h>
#include <string.h>
#include "frotz.h"

#ifdef MSDOS_16BIT

#include <alloc.h>

#define malloc(size)	farmalloc (size)
#define realloc(size,p)	farrealloc (size,p)
#define free(size)	farfree (size)
#define memcpy(d,s,n)	_fmemcpy (d,s,n)

#else

#include <stdlib.h>

#ifndef SEEK_SET
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
#endif

#define far

#endif

#define get_c fgetc

/*
 * externs
 */

extern int os_storyfile_seek(FILE * fp, long offset, int whence);

typedef unsigned long zlong;

/*
 * This is used only by save_quetzal. It probably should be allocated
 * dynamically rather than statically.
 */

static zword frames[STACK_SIZE/4+1];

/*
 * ID types.
 */

#define makeid(a,b,c,d) ((zlong) (((zlong)(a)<<24) | ((zlong)(b)<<16) | ((zlong)(c)<<8) | (zlong)(d)))

#define ID_FORM makeid ('F','O','R','M')
#define ID_IFZS makeid ('I','F','Z','S')
#define ID_IFhd makeid ('I','F','h','d')
#define ID_UMem makeid ('U','M','e','m')
#define ID_CMem makeid ('C','M','e','m')
#define ID_Stks makeid ('S','t','k','s')
#define ID_ANNO makeid ('A','N','N','O')

/*
 * Various parsing states within restoration.
 */

#define GOT_HEADER	0x01
#define GOT_STACK	0x02
#define GOT_MEMORY	0x04
#define GOT_NONE	0x00
#define GOT_ALL		0x07
#define GOT_ERROR	0x80

/*
 * Macros used to write the files.
 */

static void write_byte (unsigned char *s, zbyte b) {
  *s = b;
}

static void write_bytx (unsigned char *s, zbyte b) {
  *s = b & 0xFF;
}

static void write_word (unsigned char *s, zword w) {
  write_bytx(s,   w >> 8);
  write_bytx(s+1, w);
}

static void write_long (unsigned char *s, zlong l) {
  write_bytx(s,   l >> 24);
  write_bytx(s+1, l >> 16);
  write_bytx(s+2, l >>  8);
  write_bytx(s+3, l);
}

static void write_chnk (unsigned char *s, zlong id, zlong len) {
  write_long(s, id);
  write_long(s+4, len);
}

static void write_run(unsigned char*s, zbyte run) {
  write_byte(s, 0);
  write_byte(s+1, run);
}

/* Read one word from file; return TRUE if OK. */
static bool read_word (unsigned char *f, zword *result)
{
    int a, b;

    a = (int) *f;
    b = (int) *(f+1);

    *result = ((zword) a << 8) | (zword) b;
    return TRUE;
}

/* Read one long from file; return TRUE if OK. */
static bool read_long (unsigned char *f, zlong *result)
{
    int a, b, c, d;

    a = (int) *f;
    b = (int) *(f+1);
    c = (int) *(f+2);
    d = (int) *(f+3);

    *result = ((zlong) a << 24) | ((zlong) b << 16) |
	      ((zlong) c <<  8) |  (zlong) d;
    return TRUE;
}


/*
 * Restore a saved game using Quetzal format. Return 2 if OK, 0 if an error
 * occurred before any damage was done, -1 on a fatal error.
 */
zword restore_squetzal (unsigned char *svf, unsigned char *stf)
{
    zlong ifzslen, currlen, tmpl;
    zlong pc;
    zword i, tmpw;
    zword fatal = 0;	/* Set to -1 when errors must be fatal. */
    zbyte skip, progress = GOT_NONE;
    int x, y;
    unsigned char *stf_start = stf;

    if (svf == NULL || stf == NULL) {
      return 0;
    }

    /* Check it's really an `IFZS' file. */
    read_long (svf, &tmpl); svf += 4;
    read_long (svf, &ifzslen); svf += 4;
    read_long (svf, &currlen); svf += 4;

    if (tmpl != ID_FORM || currlen != ID_IFZS)
    {
      printf ("This is not a saved game file!\n");
      return 0;
    }

    if ((ifzslen & 1) || ifzslen<4) {/* Sanity checks. */
      printf ("ifzslen error\n");
      return 0;
    }
    ifzslen -= 4;

    /* Read each chunk and process it. */
    while (ifzslen > 0)
    {
      // printf("ifzslen %ld\n",ifzslen);
      /* Read chunk header. */
      if (ifzslen < 8) {/* Couldn't contain a chunk. */
        printf("Error couldn't contain a chunck\n");
        return 0;
      }
      read_long (svf, &tmpl); svf += 4;
      // printf("tmpl %ld\n",tmpl);

      read_long (svf, &currlen); svf += 4;
      // printf("currlen %ld\n",currlen);

      ifzslen -= 8;	/* Reduce remaining by size of header. */

      /* Handle chunk body. */
      if (ifzslen < currlen) { /* Chunk goes past EOF?! */
        printf("Chunk past EOF\n");
        return 0;
      }
      skip = currlen & 1;
      ifzslen -= currlen + (zlong) skip;

      switch (tmpl)
      {
        /* `IFhd' header chunk; must be first in file. */
        case ID_IFhd:
        // printf("ID_IFhd\n");
          if (progress & GOT_HEADER)
          {
            printf ("Save file has two IFZS chunks!\n");
            return fatal;
          }
          progress |= GOT_HEADER;
          if (currlen < 13) {
            printf ("currlen < 13\n");
            return fatal;
          }
          read_word (svf, &tmpw); svf += 2;
          if (tmpw != h_release)
            progress = GOT_ERROR;

          for (i=H_SERIAL; i<H_SERIAL+6; ++i)
          {
            x = (int) *svf; svf++;
            if (x != zmp[i])
              progress = GOT_ERROR;
          }

          read_word (svf, &tmpw); svf += 2;
          if (tmpw != h_checksum)
            progress = GOT_ERROR;

          if (progress & GOT_ERROR)
          {
            printf ("File was not saved from this story!\n");
            return fatal;
          }
          x = (int) *svf; svf++;
          pc = (zlong) x << 16;
          x = (int) *svf; svf++;
          pc |= (zlong) x << 8;
          x = (int) *svf; svf++;
          pc |= (zlong) x;
          fatal = -1;	/* Setting PC means errors must be fatal. */
          SET_PC (pc);
          // printf("PC %ld\n",pc);

          for (i=13; i<currlen; ++i)
            svf++;	// Skip rest of chunk.
          break;
          /* `Stks' stacks chunk; restoring this is quite complex. ;) */
        case ID_Stks:
        // printf("ID_Stks\n");

          if (progress & GOT_STACK)
          {
            printf ("File contains two stack chunks!\n");
            break;
          }
          progress |= GOT_STACK;

          fatal = -1;	/* Setting SP means errors must be fatal. */
          sp = stack + STACK_SIZE;

		/*
		 * All versions other than V6 may use evaluation stack outside
		 * any function context. As a result a faked function context
		 * will be present in the file here. We skip this context, but
		 * load the associated stack onto the stack proper...
		 */
		if (h_version != V6)
		{
          if (currlen < 8) {
            printf("currlen < 8\n");
            return fatal;
          }
		    for (i=0; i<6; ++i) {
              if (((int) *svf) != 0) {
                printf("svf != 0\n");
                return fatal;
              }
              svf++;
            }
            read_word (svf, &tmpw); svf += 2;
		    /* if (!read_word (svf, &tmpw))		return fatal; */
		    if (tmpw > STACK_SIZE)
		    {
			printf ("Save-file has too much stack (and I can't cope).\n");
			return fatal;
		    }
		    currlen -= 8;
		    if (currlen < tmpw*2) {
              printf("currlen < tmpw*2\n");
              return fatal;
            }
		    for (i=0; i<tmpw; ++i) {
              read_word (svf, --sp); svf += 2;
            }
			/* if (!read_word (svf, --sp))		return fatal; */
		    currlen -= tmpw*2;
		}

		/* We now proceed to load the main block of stack frames. */
		for (fp = stack+STACK_SIZE, frame_count = 0;
		     currlen > 0;
		     currlen -= 8, ++frame_count)
		{
          if (currlen < 8) {
            printf("currlen < 8\n");
            return fatal;
          }
		    if (sp - stack < 4)	/* No space for frame. */
		    {
			printf ("Save-file has too much stack (and I can't cope).\n");
			return fatal;
		    }

		    /* Read PC, procedure flag and formal param count. */
            read_long (svf, &tmpl); svf += 4;
		    /* if (!read_long (svf, &tmpl))		return fatal; */
		    y = (int) (tmpl & 0x0F);	/* Number of formals. */
		    tmpw = y << 8;

		    /* Read result variable. */
            x = (int) *svf; svf++;
		    /* if ((x = get_c (svf)) == EOF)		return fatal; */

		    /* Check the procedure flag... */
		    if (tmpl & 0x10)
		    {
			tmpw |= 0x1000;	/* It's a procedure. */
			tmpl >>= 8;	/* Shift to get PC value. */
		    }
		    else
		    {
			/* Functions have type 0, so no need to or anything. */
			tmpl >>= 8;	/* Shift to get PC value. */
			--tmpl;		/* Point at result byte. */
			/* Sanity check on result variable... */
			if (zmp[tmpl] != (zbyte) x)
			{
			    printf ("Save-file has wrong variable number on stack (possibly wrong game version?)\n");
			    return fatal;
			}
		    }
		    *--sp = (zword) (tmpl >> 9);	/* High part of PC */
		    *--sp = (zword) (tmpl & 0x1FF);	/* Low part of PC */
		    *--sp = (zword) (fp - stack - 1);	/* FP */

		    /* Read and process argument mask. */
            x = (int) *svf; svf++;
		    /* if ((x = get_c (svf)) == EOF)		return fatal; */
		    ++x;	/* Should now be a power of 2 */
		    for (i=0; i<8; ++i)
			if (x & (1<<i))
			    break;
		    if (x ^ (1<<i))	/* Not a power of 2 */
		    {
			printf ("Save-file uses incomplete argument lists (which I can't handle)\n");
			return fatal;
		    }
		    *--sp = tmpw | i;
		    fp = sp;	/* FP for next frame. */

		    /* Read amount of eval stack used. */
            read_word (svf, &tmpw); svf += 2;
		    /* if (!read_word (svf, &tmpw))		return fatal; */

		    tmpw += y;	/* Amount of stack + number of locals. */
		    if (sp - stack <= tmpw)
		    {
			printf ("Save-file has too much stack (and I can't cope).\n");
			return fatal;
		    }
		    if (currlen < tmpw*2) {
              printf("currlen < tmpw*2\n");
              return fatal;
            }
		    for (i=0; i<tmpw; ++i) {
              read_word (svf, --sp); svf += 2;
            }
			/* if (!read_word (svf, --sp))		return fatal; */
		    currlen -= tmpw*2;
		}
		/* End of `Stks' processing... */
		break;
	    /* Any more special chunk types must go in HERE or ABOVE. */
	    /* `CMem' compressed memory chunk; uncompress it. */
	    case ID_CMem:
      // printf("ID_CMem\n");
		if (!(progress & GOT_MEMORY))	/* Don't complain if two. */
		{
        stf = stf_start;
		    // (void) os_storyfile_seek (stf, 0, SEEK_SET);
		    i=0;	/* Bytes written to data area. */
		    for (; currlen > 0; --currlen)
		    {
              x = (int) *svf; svf++;
			/* if ((x = get_c (svf)) == EOF)		return fatal; */
			if (x == 0)	/* Start run. */
			{
			    /* Check for bogus run. */
			    if (currlen < 2)
			    {
				printf ("File contains bogus `CMem' chunk.\n");
				for (; currlen > 0; --currlen)
                  svf++;
				    /* (void) get_c (svf);	/\* Skip rest. *\/ */
				currlen = 1;
				i = 0xFFFF;
				break; /* Keep going; may be a `UMem' too. */
			    }
			    /* Copy story file to memory during the run. */
			    --currlen;
                x = (int) *svf; svf++;
			    /* if ((x = get_c (svf)) == EOF)	return fatal; */
			    for (; x >= 0 && i<h_dynamic_size; --x, ++i) {
            y = (int) *stf; stf++;
            zmp[i] = (zbyte) y;
          }
			}
			else	/* Not a run. */
			{
        y = (int) *stf; stf++;
              // if ((y = get_c (stf)) == EOF) {
              //   printf("get_c (stf) == EOF\n");
              //   return fatal;
              // }
			    zmp[i] = (zbyte) (x ^ y);
			    ++i;
			}
			/* Make sure we don't load too much. */
			if (i > h_dynamic_size)
			{
			    printf ("warning: `CMem' chunk too long!\n");
			    for (; currlen > 1; --currlen)
                  svf++;
				/* (void) get_c (svf);	/\* Skip rest. *\/ */
			    break;	/* Keep going; there may be a `UMem' too. */
			}
		    }
		    /* If chunk is short, assume a run. */
		    for (; i<h_dynamic_size; ++i) {
          y = (int) *stf; stf++;
          zmp[i] = (zbyte) y;
        }
		    if (currlen == 0)
			progress |= GOT_MEMORY;	/* Only if succeeded. */
		    break;
	    }
		/* Fall right thru (to default) if already GOT_MEMORY */
	    /* `UMem' uncompressed memory chunk; load it. */
	    case ID_UMem:
      // printf("ID_UMem\n");
		if (!(progress & GOT_MEMORY))	/* Don't complain if two. */
		{
		    /* Must be exactly the right size. */
		    if (currlen == h_dynamic_size)
		    {
              printf("Made it to sketch memcpy\n");
              memcpy(zmp, svf, currlen); // Do we need currlen * sizeof(zword)?
              svf += currlen;
              progress |= GOT_MEMORY;	/* Only on success. */
              break;
			}
		    /* Fall into default action (skip chunk) on errors. */
		}
		/* Fall thru (to default) if already GOT_MEMORY */
	    /* Unrecognised chunk type; skip it. */
	    default:
          svf += currlen;
		/* (void) fseek (svf, currlen, SEEK_CUR);	/\* Skip chunk. *\/ */
		      break;
	} // switch
	if (skip)
      svf++;
	    /* (void) get_c (svf);	/\* Skip pad byte. *\/ */
    } // while

    /*
     * We've reached the end of the file. For the restoration to have been a
     * success, we must have had one of each of the required chunks.
     */
    if (!(progress & GOT_HEADER))
	printf ("error: no valid header (`IFhd') chunk in file.\n");
    if (!(progress & GOT_STACK))
	printf ("error: no valid stack (`Stks') chunk in file.\n");
    if (!(progress & GOT_MEMORY))
	printf ("error: no valid memory (`CMem' or `UMem') chunk in file.\n");

    return (progress == GOT_ALL ? 2 : fatal);
}


/*
 * Save a game using Quetzal format. Return 1 if OK, 0 if failed.
 */
zword save_squetzal (unsigned char *svf, unsigned char *stf)
{
    zlong ifzslen = 0, cmemlen = 0, stkslen = 0;
    zlong pc;
    zword i, j, n;
    zword nvars, nargs, nstk, *p;
    zbyte var;
    long start, cmempos, stkspos;
    int c;

    if (svf == NULL || stf == NULL) {
      return 0;
    }

    start = (long) svf;
    /* Write `IFZS' header. */
    write_chnk (svf, ID_FORM, 0); svf += 8;
    write_long (svf, ID_IFZS); svf += 4;

    /* Write `IFhd' chunk. */
    GET_PC (pc);
    write_chnk (svf, ID_IFhd, 13); svf += 8;
    write_word (svf, h_release); svf += 2;
    for (i=H_SERIAL; i<H_SERIAL+6; ++i) {
      write_byte (svf, zmp[i]); svf++;
    }
    write_word (svf, h_checksum); svf += 2;
    write_long (svf, pc << 8); svf += 4; /* Includes pad. */

    /* Write `CMem' chunk. */
    cmempos = (long) svf;
    write_chnk (svf, ID_CMem, 0); svf += 8;
    // (void) os_storyfile_seek (stf, 0, SEEK_SET);
    /* j holds current run length. */
    for (i=0, j=0, cmemlen=0; i < h_dynamic_size; ++i)
    {
      c = (int) *stf; stf++;
	// if ((c = get_c (stf)) == EOF)			return 0;
	c ^= (int) zmp[i];
	if (c == 0)
	    ++j;	/* It's a run of equal bytes. */
	else
	{
	    /* Write out any run there may be. */
	    if (j > 0)
	    {
		for (; j > 0x100; j -= 0x100)
		{
          write_run (svf, 0xFF); svf += 2;
		    cmemlen += 2;
		}
		write_run (svf, j-1); svf += 2;
		cmemlen += 2;
		j = 0;
	    }
	    /* Any runs are now written. Write this (nonzero) byte. */
	    write_byte (svf, (zbyte) c); svf++;
	    ++cmemlen;
	}
    }

    /*
     * Reached end of dynamic memory. We ignore any unwritten run there may be
     * at this point.
     */
    if (cmemlen & 1) {	/* Chunk length must be even. */
      write_byte (svf, 0); svf++;
    }

    /* Write `Stks' chunk. You are not expected to understand this. ;) */
    stkspos = (long) svf;
    write_chnk (svf, ID_Stks, 0); svf += 8;

    /*
     * We construct a list of frame indices, most recent first, in `frames'.
     * These indices are the offsets into the `stack' array of the word before
     * the first word pushed in each frame.
     */
    frames[0] = sp - stack;	/* The frame we'd get by doing a call now. */
    for (i = fp - stack + 4, n=0; i < STACK_SIZE+4; i = stack[i-3] + 5)
	frames[++n] = i;

    /*
     * All versions other than V6 can use evaluation stack outside a function
     * context. We write a faked stack frame (most fields zero) to cater for
     * this.
     */
    if (h_version != V6)
    {
      for (i=0; i<6; ++i) {
        write_byte (svf, 0); svf++;
      }
	nstk = STACK_SIZE - frames[n];
	write_word (svf, nstk); svf += 2;
	for (j=STACK_SIZE-1; j >= frames[n]; --j) {
      write_word (svf, stack[j]); svf += 2;
    }
	stkslen = 8 + 2*nstk;
    }

    /* Write out the rest of the stack frames. */
    for (i=n; i>0; --i)
    {
	p = stack + frames[i] - 4;	/* Points to call frame. */
	nvars = (p[0] & 0x0F00) >> 8;
	nargs =  p[0] & 0x00FF;
	nstk  =  frames[i] - frames[i-1] - nvars - 4;
	pc    =  ((zlong) p[3] << 9) | p[2];

	switch (p[0] & 0xF000)	/* Check type of call. */
	{
	    case 0x0000:	/* Function. */
		var = zmp[pc];
		pc = ((pc + 1) << 8) | nvars;
		break;
	    case 0x1000:	/* Procedure. */
		var = 0;
		pc = (pc << 8) | 0x10 | nvars;	/* Set procedure flag. */
		break;
	    /* case 0x2000: */
	    default:
		runtime_error (ERR_SAVE_IN_INTER);
		return 0;
	}
	if (nargs != 0)
	    nargs = (1 << nargs) - 1;	/* Make args into bitmap. */

	/* Write the main part of the frame... */
	write_long (svf, pc); svf += 4;
	write_byte (svf, var); svf++;
	write_byte (svf, nargs); svf++;
	write_word (svf, nstk); svf += 2;

	/* Write the variables and eval stack. */
	for (j=0, --p; j<nvars+nstk; ++j, --p) {
      write_word (svf, *p); svf += 2;
    }

	/* Calculate length written thus far. */
	stkslen += 8 + 2 * (nvars + nstk);
    }

    /* Fill in variable chunk lengths. */
    ifzslen = 3*8 + 4 + 14 + cmemlen + stkslen;
    if (cmemlen & 1)
	++ifzslen;
    svf = (unsigned char *) (start + 4);
    /* (void) fseek (svf,         4, SEEK_SET); */
    write_long (svf, ifzslen); svf += 4;
    svf = (unsigned char *) cmempos + 4;
    /* (void) fseek (svf, cmempos+4, SEEK_SET); */
    write_long (svf, cmemlen); svf += 4;
    svf = (unsigned char *) (stkspos + 4);
    /* (void) fseek (svf, stkspos+4, SEEK_SET); */
    write_long (svf, stkslen); svf += 4;

    /* After all that, still nothing went wrong! */
    return 1;
}
