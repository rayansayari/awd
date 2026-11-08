package com.carrental.payment.service;

import com.carrental.payment.dto.*;

public interface PaymentService {
    PaymentResponse processPayment(PaymentRequest req);
    PaymentResponse getPaymentById(Long id);
    PaymentResponse getPaymentByReservation(Long reservationId);
    PaymentResponse refundPayment(Long reservationId);
}
