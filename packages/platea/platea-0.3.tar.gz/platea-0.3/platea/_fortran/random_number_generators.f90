! ##############################################################################
! rng

module rng

  use types ! set type precision

  ! user has default access to all functions
  public

  ! ############################################################################
  ! set the defualt rnadom number generator

  interface ran
    module procedure ran2
  end interface

  integer, parameter :: state_size = 35

  ! ############################################################################

  contains

    ! ##########################################################################
    ! ##########################################################################

    function ran0(state) result(o)
      ! Numerical Recipes in Fortran77 Ch7.1 <ran0>
      ! Numerical Recipes in C 2Ed Ch7.1 <ran0>

      integer(dp) state(1), k
      real(dp) o

      integer(dp), parameter :: ia = 16807, im = 2147483647, iq = 127773, &
        ir = 2836, mask = 123459876
      real(dp), parameter :: am = 1. / im

      state(1) = ieor(state(1), mask)
      k = state(1) / iq
      state(1) = ia * (state(1) - k * iq) - ir * k
      if (state(1).lt.0) state(1) = state(1) + im
      o = am * state(1)
      state(1) = ieor(state(1), mask)

      return
    end

    subroutine ran0v(state, new_state, output, n)
      ! wrapper for python

      integer(dp) state(1), new_state(1) ! seed size
      real(dp) output(n)

      !f2py intent(in) :: state, n
      !f2py intent(out) :: new_state, output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one) ! x % 2n == x & (2n - 1)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = ran0(state) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = ran0(state) ! function reference
      end do

      new_state  = state

    end subroutine ran0v

    subroutine ran0v2(state, new_state, output, n, m)
      ! wrapper for python

      integer(dp) state(1), new_state(1) ! seed size
      real(dp) output(n, m)

      !f2py intent(in) :: state, n, m
      !f2py intent(out) :: new_state, output

      integer(sp) :: n, m, remainder, remainder2
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      remainder2 = iand(m, unroll_minus_one)

      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1

          do i2 = 1, m - remainder, unroll
            do j2 = 1, unroll, 1
              output(i+j-1, i2+j2-1) = ran0(state) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = ran0(state) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = ran0(state) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = ran0(state) ! function reference
        end do

      end do

      new_state  = state

    end subroutine ran0v2

    ! ##########################################################################
    ! ##########################################################################

    function ran1(state) result(o)
      ! Numerical Recipes in Fortran77 Ch7.1 <ran1>
      ! Numerical Recipes in C 2Ed Ch7.1 <ran1>

      use types

      integer(dp) state(34)
      integer(dp) idum, ia, im, iq, ir, ntab, ndiv
      real(dp) o, am, eps, rnmx

      parameter (ia = 16807_dp, im = 2147483647_dp, am = 1.0_dp / im, &
        iq = 127773_dp, ir = 2836_dp, ntab = 32, &
        ndiv = 1.0_dp + (im - 1.0_dp) / ntab, eps =1.2e-7, rnmx = 1.0_dp - eps)

      integer(dp) j, k, iv(ntab), iy

      idum = state(1)
      iv = state(2:size(state)-1)
      iy = state(size(state))

      if (idum.le.0_dp.or.iy.eq.0_dp) then
        idum = max(-idum, 1)

        ! if (-idum < 1_dp) then
        !   idum = 1_dp
        ! else
        !   idum = -idum
        ! end if

        do 11 j = ntab+8, 1, -1
          k = idum / iq
          idum = ia * (idum - k * iq) - ir * k
          if (idum.lt.0_dp) idum = idum + im
          if (j.le.ntab) iv(j) = idum
        11 continue
        iy = iv(1)
      endif

      k = idum / iq
      idum = ia * (idum - k * iq) - ir * k
      if (idum.lt.0_dp) idum = idum + im
      j = 1.0_dp + iy / ndiv
      iy = iv(j)
      iv(j) = idum
      o = min(am * iy, rnmx)
      !o = real(o, dp)

      state(1) = idum
      state(2:size(state)-1) = iv
      state(size(state)) = iy

      return
    end

    subroutine ran1v(state, new_state, output, n)
      ! wrapper for python

      integer(dp) state(34), new_state(34) ! seed size
      real(dp) output(n)

      !f2py intent(in) :: state, n
      !f2py intent(out) :: new_state, output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = ran1(state) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = ran1(state) ! function reference
      end do

      new_state  = state

    end subroutine ran1v

    subroutine ran1v2(state, new_state, output, n, m)
      ! wrapper for python

      integer(dp) state(34), new_state(34) ! seed size
      real(dp) output(n, m)

      !f2py intent(in) :: state, n, m
      !f2py intent(out) :: new_state, output

      integer(sp) :: n, m, remainder, remainder2
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      remainder2 = iand(m, unroll_minus_one)

      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1

          do i2 = 1, m - remainder, unroll
            do j2 = 1, unroll, 1
              output(i+j-1, i2+j2-1) = ran1(state) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = ran1(state) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = ran1(state) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = ran1(state) ! function reference
        end do

      end do

      new_state  = state

    end subroutine ran1v2

    ! ##########################################################################
    ! ##########################################################################

    function ran2(state) result(o)
      ! Numerical Recipes in Fortran77 Ch7.1 <ran2>
      ! Numerical Recipes in C 2Ed Ch7.1 <ran2>

      use types

      integer(dp) state(35)
      integer(dp) idum, im1, im2, imm1, ia1, ia2, iq1, iq2, ir1, ir2, ntab, ndiv
      real(dp) am, eps, rnmx,  o

      parameter (im1 = 2147483563, im2 = 2147483399, am = 1. / im1, &
        imm1 = im1 - 1, ia1 = 40014, ia2 = 40692, iq1 = 53668, iq2 = 52774, &
        ir1 = 12211, ir2 = 3791, ntab = 32, ndiv = 1 + imm1 / ntab, &
        eps = 1.2e-7, rnmx = 1. - eps)

      integer idum2, j ,k, iv(ntab), iy

      idum = state(1)
      iv = state(2:size(state)-2)
      iy = state(size(state)-1)
      idum2 = state(size(state))

      if (idum.le.0) then
        idum = max(-idum, 1)

        ! if (-idum < 1.0) then
        !   idum = 1
        ! else
        !   idum = -idum
        ! end if

        idum2 = idum

        do 11 j = ntab + 8, 1, -1
          k = idum / iq1
          idum = ia1 * (idum - k * iq1) - k * ir1
          if (idum.lt.0) idum = idum + im1
          if (j.le.ntab) iv(j) = idum
        11 continue
        iy = iv(1)
      endif

      k = idum / iq1
      idum = ia1 * (idum - k * iq1) - k * ir1
      if (idum.lt.0) idum = idum + im1
      k = idum2 / iq2
      idum2 = ia2 * (idum2 - k * iq2) - k * ir2
      if (idum2.lt.0) idum2 = idum2 + im2
      j = 1 + iy / ndiv
      iy = iv(j) - idum2
      iv(j) = idum
      if(iy.lt.1) iy = iy + imm1
      o = min(am * iy, rnmx)

      state(1) = idum
      state(2:size(state)-2) = iv
      state(size(state)-1) = iy
      state(size(state)) = idum2

      return
    end

    subroutine ran2v(state, new_state, output, n)
      ! wrapper for python

      integer(dp) state(35), new_state(35) ! seed size
      real(dp) output(n)

      !f2py intent(in) :: state, n
      !f2py intent(out) :: new_state, output

      integer(sp) :: n, remainder
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1
          output(i+j-1) = ran2(state) ! function reference
        end do
      end do
      do i = n - remainder + 1, n, 1
        output(i) = ran2(state) ! function reference
      end do

      new_state  = state

    end subroutine ran2v

    subroutine ran2v2(state, new_state, output, n, m)
      ! wrapper for python

      integer(dp) state(35), new_state(35) ! seed size
      real(dp) output(n, m)

      !f2py intent(in) :: state, n, m
      !f2py intent(out) :: new_state, output

      integer(sp) :: n, m, remainder, remainder2
      integer(sp), parameter :: unroll = 8, unroll_minus_one = 7

      remainder = iand(n, unroll_minus_one)
      remainder2 = iand(m, unroll_minus_one)

      do i = 1, n - remainder, unroll
        do j = 1, unroll, 1

          do i2 = 1, m - remainder, unroll
            do j2 = 1, unroll, 1
              output(i+j-1, i2+j2-1) = ran2(state) ! function reference
            end do
          end do

          do i2 = m - remainder + 1, m, 1
            output(i+j-1, i2) = ran2(state) ! function reference
          end do

        end do
      end do

      do i = n - remainder + 1, n, 1

        do i2 = 1, m - remainder, unroll
          do j2 = 1, unroll, 1
            output(i, i2+j2-1) = ran2(state) ! function reference
          end do
        end do

        do i2 = m - remainder + 1, m, 1
          output(i, i2) = ran2(state) ! function reference
        end do

      end do

      new_state  = state

    end subroutine ran2v2

    ! ##########################################################################
    ! ##########################################################################

end module rng
