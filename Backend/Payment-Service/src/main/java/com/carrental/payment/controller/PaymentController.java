package com.carrental.payment.controller;

import com.carrental.payment.dto.*;
import com.carrental.payment.service.PaymentService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/payments")
@RequiredArgsConstructor
public class PaymentController {
    private final PaymentService paymentService;

    @PostMapping("/process")
    public ResponseEntity<PaymentResponse> process(@Valid @RequestBody PaymentRequest req) {
        return new ResponseEntity<>(paymentService.processPayment(req), HttpStatus.CREATED);
    }

    @GetMapping("/{id}")
    public ResponseEntity<PaymentResponse> getById(@PathVariable Long id) {
        return ResponseEntity.ok(paymentService.getPaymentById(id));
    }

    @GetMapping("/reservation/{reservationId}")
    public ResponseEntity<PaymentResponse> getByReservation(@PathVariable Long reservationId) {
        return ResponseEntity.ok(paymentService.getPaymentByReservation(reservationId));
    }

    @PostMapping("/refund/{reservationId}")
    public ResponseEntity<PaymentResponse> refund(@PathVariable Long reservationId) {
        return ResponseEntity.ok(paymentService.refundPayment(reservationId));
    }
}
