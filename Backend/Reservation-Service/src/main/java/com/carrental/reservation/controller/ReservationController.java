package com.carrental.reservation.controller;

import com.carrental.reservation.dto.*;
import com.carrental.reservation.service.ReservationService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/reservations")
@RequiredArgsConstructor
public class ReservationController {
    private final ReservationService reservationService;

    @PostMapping
    public ResponseEntity<ReservationResponse> create(@Valid @RequestBody ReservationRequest req) {
        return new ResponseEntity<>(reservationService.createReservation(req), HttpStatus.CREATED);
    }

    @GetMapping("/{id}")
    public ResponseEntity<ReservationResponse> getById(@PathVariable Long id) {
        return ResponseEntity.ok(reservationService.getReservationById(id));
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<List<ReservationResponse>> getByUser(@PathVariable Long userId) {
        return ResponseEntity.ok(reservationService.getUserReservations(userId));
    }

    @PutMapping("/{id}/confirm")
    public ResponseEntity<ReservationResponse> confirm(@PathVariable Long id) {
        return ResponseEntity.ok(reservationService.confirmReservation(id));
    }

    @PutMapping("/{id}/cancel")
    public ResponseEntity<ReservationResponse> cancel(@PathVariable Long id) {
        return ResponseEntity.ok(reservationService.cancelReservation(id));
    }
}
