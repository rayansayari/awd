package com.carrental.reservation.service;

import com.carrental.reservation.dto.*;
import java.util.List;

public interface ReservationService {
    ReservationResponse createReservation(ReservationRequest req);
    ReservationResponse getReservationById(Long id);
    List<ReservationResponse> getUserReservations(Long userId);
    ReservationResponse confirmReservation(Long id);
    ReservationResponse cancelReservation(Long id);
}
