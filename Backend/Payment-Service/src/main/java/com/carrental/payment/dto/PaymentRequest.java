package com.carrental.payment.dto;

import com.carrental.payment.domain.PaymentMethod;
import jakarta.validation.constraints.NotNull;
import lombok.*;
import java.math.BigDecimal;

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class PaymentRequest {
    @NotNull
    private Long reservationId;

    @NotNull
    private Long userId;

    @NotNull
    private BigDecimal amount;

    @Builder.Default
    private PaymentMethod method = PaymentMethod.CREDIT_CARD;
}
