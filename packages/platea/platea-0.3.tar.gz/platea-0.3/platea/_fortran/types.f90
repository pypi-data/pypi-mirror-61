module types
  ! should replace .f2py_f2cmap

  implicit none

  ! fortran 2008 specific
  !use, intrinsic :: iso_fortran_env
  !integer, parameter :: sp = REAL32
  !integer, parameter :: dp = REAL64
  !integer, parameter :: qp = REAL128

  integer, parameter :: sp = selected_real_kind(6, 37) ! 32 single
  !integer, parameter :: dp = selected_real_kind(15, 307) ! 64 double
  integer, parameter :: qp = selected_real_kind(33, 4931) ! 128 quadruple

  !machine specific double precision
  integer, parameter :: dp = kind(1.d0)

  real(sp) :: r_sp = 1.0
  real(dp) :: r_dp = 1.0_dp
  real(qp) :: r_qp = 1.0_qp

end module


module precision

  use types ! set type precision

  contains

    subroutine get_integer_precision()
      !implicit none

      integer(sp) :: single
      integer(dp) :: double
      integer(qp) :: quadruple

      print *, "Huge Integer Single Precision"
      print *, huge(single)
      print *, "Huge Integer Double Precision"
      print *, huge(double)
      print *, "Huge Integer Quadruple Precision"
      print *, huge(quadruple)

    end subroutine get_integer_precision

    subroutine get_real_precision()
      !implicit none

      real(sp) :: single
      real(dp) :: double
      real(qp) :: quadruple

      print *, "Huge Real Single Precision"
      print *, huge(single)
      print *, "Huge Real Double Precision"
      print *, huge(double)
      print *, "Huge Real Quadruple Precision"
      print *, huge(quadruple)

      print *, "Tiny Real Single Precision"
      print *, tiny(single)
      print *, "Tiny Real Double Precision"
      print *, tiny(double)
      print *, "Tiny Real Quadruple Precision"
      print *, tiny(quadruple)

    end subroutine get_real_precision

end module
