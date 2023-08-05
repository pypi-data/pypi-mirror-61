/*
   Copyright (C) 2011  Equinor ASA, Norway.

   The file 'sched_kw_wconinjh.h' is part of ERT - Ensemble based Reservoir Tool.

   ERT is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   ERT is distributed in the hope that it will be useful, but WITHOUT ANY
   WARRANTY; without even the implied warranty of MERCHANTABILITY or
   FITNESS FOR A PARTICULAR PURPOSE.

   See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html>
   for more details.
*/

#ifndef ERT_SCHED_KW_WCONINJH_H
#define ERT_SCHED_KW_WCONINJH_H
#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>
#include <stdbool.h>

#include <ert/util/time_t_vector.hpp>
#include <ert/util/hash.hpp>
#include <ert/util/stringlist.hpp>

#include <ert/sched/sched_macros.hpp>
#include <ert/sched/sched_types.hpp>



typedef struct sched_kw_wconhist_struct sched_kw_wconinjh_type;
typedef struct wconinjh_state_struct    wconinjh_state_type;

sched_kw_wconinjh_type * sched_kw_wconinjh_fscanf_alloc( FILE *, bool *, const char *);
void                     sched_kw_wconinjh_free(sched_kw_wconinjh_type * );
void                     sched_kw_wconinjh_fprintf(const sched_kw_wconinjh_type * , FILE *);
void                     sched_kw_wconinjh_fwrite(const sched_kw_wconinjh_type *, FILE *);
sched_kw_wconinjh_type * sched_kw_wconinjh_fread_alloc( FILE *);

hash_type              * sched_kw_wconinjh_alloc_well_obs_hash(const sched_kw_wconinjh_type *);

void                     sched_kw_wconinjh_update_state( const sched_kw_wconinjh_type * kw , wconinjh_state_type * state , const char * well_name , int report_step );
wconinjh_state_type    * wconinjh_state_alloc( const time_t_vector_type * time);
void                     wconinjh_state_free( wconinjh_state_type * wconinjh );
void                     sched_kw_wconinjh_close_state(wconinjh_state_type * state , int report_step );

sched_phase_enum         wconinjh_state_iget_phase( const wconinjh_state_type * state , int report_step);

/*******************************************************************/
KW_HEADER(wconinjh)

#ifdef __cplusplus
}
#endif
#endif
