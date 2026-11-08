package com.carrental.reservation.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.*;
import java.math.BigDecimal;
import java.util.Map;

@FeignClient(name = "vehicle-service")
public interface VehicleClient {
    @GetMapping("/api/vehicles/{id}")
    Map<String, Object> getVehicleById(@PathVariable("id") Long id);

    @GetMapping("/api/vehicles/{id}/availability")
    Map<String, Object> checkAvailability(@PathVariable("id") Long id);

    @PatchMapping("/api/vehicles/{id}/status")
    void updateStatus(@PathVariable("id") Long id, @RequestParam("status") String status);
}
