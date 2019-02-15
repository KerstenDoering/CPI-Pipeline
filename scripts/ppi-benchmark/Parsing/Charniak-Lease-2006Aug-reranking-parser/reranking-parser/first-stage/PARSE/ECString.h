
#ifndef MECSTRING_H
#define MECSTRING_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>


#define ECS gnu

#if ECS == gnu
using namespace std;
#include <string>
#define ECString string
#else
#include <bstring.h>
#define ECString string
#endif

#endif	/* ! MECSTRING_H */
