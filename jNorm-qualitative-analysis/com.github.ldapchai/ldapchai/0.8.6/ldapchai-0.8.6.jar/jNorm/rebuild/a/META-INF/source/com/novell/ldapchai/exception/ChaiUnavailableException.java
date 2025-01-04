/*
 * LDAP Chai API
 * Copyright (c) 2006-2017 Novell, Inc.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

package com.novell.ldapchai.exception;

/**
 * An exception indicating that the directory was unreachable.  The underlying message and/or error code is inferred
 * from responses generated by the ldap server or underlying API such as JNDI.
 *
 * @author Jason D. Rivard
 * @see ChaiError
 */
public class ChaiUnavailableException extends ChaiException
{
    /**
     * Generate a new {@code ChaiUnavailableException} based on the supplied
     * error message.  The message is scanned for known {@link ChaiError}
     * error codes.  If found, the correct {@code ChaiErrorCode} will be used. Otherwise,
     * {@link ChaiError#UNKNOWN} will be used.
     *
     * @param errorMessage string containing an error description/code
     * @return valid error code for the string
     */
    public static ChaiUnavailableException forErrorMessage( final String errorMessage )
    {
        return new ChaiUnavailableException( errorMessage, ChaiErrors.getErrorForMessage( errorMessage ) );
    }

    public static ChaiUnavailableException forErrorMessage( final String errorMessage, final Throwable cause )
    {
        return new ChaiUnavailableException( errorMessage, ChaiErrors.getErrorForMessage( errorMessage ), cause );
    }

    public ChaiUnavailableException( final String message, final ChaiError errorCode )
    {
        super( message, errorCode );
    }

    public ChaiUnavailableException( final String message, final ChaiError errorCode, final Throwable cause )
    {
        super( message, errorCode, cause );
    }

    public ChaiUnavailableException(
            final String message,
            final ChaiError errorCode,
            final boolean permanent,
            final boolean authentication
    )
    {
        super( message, errorCode, permanent, authentication );
    }

    public ChaiUnavailableException(
            final String message,
            final ChaiError errorCode,
            final boolean permanent,
            final boolean authentication,
            final Throwable cause
    )
    {
        super( message, errorCode, permanent, authentication, cause );
    }
}
