/******************************************************************************
*       SOFA, Simulation Open-Framework Architecture                          *
*                (c) 2006-2018 INRIA, USTL, UJF, CNRS, MGH                    *
*                                                                             *
* This library is free software; you can redistribute it and/or modify it     *
* under the terms of the GNU Lesser General Public License as published by    *
* the Free Software Foundation; either version 2.1 of the License, or (at     *
* your option) any later version.                                             *
*                                                                             *
* This library is distributed in the hope that it will be useful, but WITHOUT *
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       *
* FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License *
* for more details.                                                           *
*                                                                             *
* You should have received a copy of the GNU Lesser General Public License    *
* along with this library; if not, write to the Free Software Foundation,     *
* Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.          *
*******************************************************************************
*                            Plugin Stlib      v1.0                           *
*				                                                              *
* This plugin is also distributed under the GNU LGPL (Lesser General          *
* Public License) license with the same conditions than SOFA.                 *
*                                                                             *
* Contributors: Defrost team  (INRIA, University of Lille, CNRS,              *
*               Ecole Centrale de Lille)                                      *
*                                                                             *
* Contact information: https://project.inria.fr/softrobot/contact/            *
*                                                                             *
******************************************************************************/
#include "initPlugin.h"

#include <sofa/config/sharedlibrary_defines.h>

namespace sofa::component
{

extern "C" {
    SOFA_STLIB_API void initExternalModule();
    SOFA_STLIB_API const char* getModuleName();
    SOFA_STLIB_API const char* getModuleVersion();
    SOFA_STLIB_API const char* getModuleLicense();
    SOFA_STLIB_API const char* getModuleDescription();
    SOFA_STLIB_API const char* getModuleComponentList();
}

void initExternalModule()
{
    static bool first = true;
    if (!first)
    {
        return;
    }
    first = false;
}

const char* getModuleName()
{
    return "STLIB";
}

const char* getModuleVersion()
{
    return "3.0";
}

const char* getModuleLicense()
{
    return "LGPL";
}

const char* getModuleDescription()
{
    return "Sofa Template Library";
}

const char* getModuleComponentList()
{
    return "";
}

}
