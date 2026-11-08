package com.carrental.payment.service.impl;

import com.carrental.payment.domain.*;
import com.carrental.payment.dto.*;
import com.carrental.payment.repository.*;
import com.carrental.payment.service.PaymentService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class PaymentServiceImpl implements PaymentService {
    private final PaymentRepository paymentRepository;
    private final InvoiceRepository invoiceRepository;

    @Override
    public PaymentResponse processPayment(PaymentRequest req) {
        Payment p = Payment.builder()
                .transactionId("TX-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase())
                .reservationId(req.getReservationId())
                .userId(req.getUserId())
                .amount(req.getAmount())
                .paymentMethod(req.getMethod())
                .status(PaymentStatus.PAID) // Simulation bancaire validée
                .build();

        Payment saved = paymentRepository.save(p);

        Invoice inv = Invoice.builder()
                .invoiceNumber("INV-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase())
                .paymentId(saved.getId())
                .reservationId(saved.getReservationId())
                .totalAmount(saved.getAmount())
                .build();
        Invoice savedInv = invoiceRepository.save(inv);

        return PaymentResponse.builder()
                .id(saved.getId())
                .transactionId(saved.getTransactionId())
                .reservationId(saved.getReservationId())
                .amount(saved.getAmount())
                .status(saved.getStatus())
                .paymentDate(saved.getPaymentDate())
                .invoiceNumber(savedInv.getInvoiceNumber())
                .build();
    }

    @Override
    public PaymentResponse getPaymentById(Long id) {
        Payment p = paymentRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Paiement introuvable: " + id));
        return mapToDTO(p);
    }

    @Override
    public PaymentResponse getPaymentByReservation(Long reservationId) {
        Payment p = paymentRepository.findByReservationId(reservationId)
                .orElseThrow(() -> new RuntimeException("Paiement introuvable pour la réservation: " + reservationId));
        return mapToDTO(p);
    }

    @Override
    public PaymentResponse refundPayment(Long reservationId) {
        Payment p = paymentRepository.findByReservationId(reservationId)
                .orElseThrow(() -> new RuntimeException("Paiement introuvable: " + reservationId));
        p.setStatus(PaymentStatus.REFUNDED);
        return mapToDTO(paymentRepository.save(p));
    }

    private PaymentResponse mapToDTO(Payment p) {
        return PaymentResponse.builder()
                .id(p.getId())
                .transactionId(p.getTransactionId())
                .reservationId(p.getReservationId())
                .amount(p.getAmount())
                .status(p.getStatus())
                .paymentDate(p.getPaymentDate())
                .build();
    }
}
