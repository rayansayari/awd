package com.carrental.reservation.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import java.util.Map;

@FeignClient(name = "payment-service")
public interface PaymentClient {
    @PostMapping("/api/payments/process")
    Map<String, Object> processPayment(@RequestBody Map<String, Object> paymentReq);
}
