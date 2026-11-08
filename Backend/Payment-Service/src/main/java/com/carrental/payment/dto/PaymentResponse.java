package com.carrental.payment.dto;

import com.carrental.payment.domain.PaymentStatus;
import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class PaymentResponse {
    private Long id;
    private String transactionId;
    private Long reservationId;
    private BigDecimal amount;
    private PaymentStatus status;
    private LocalDateTime paymentDate;
    private String invoiceNumber;
}
