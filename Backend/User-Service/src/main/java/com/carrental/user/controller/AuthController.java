package com.carrental.user.controller;

import com.carrental.user.dto.*;
import com.carrental.user.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {
    private final UserService userService;

    @PostMapping("/register")
    public ResponseEntity<UserDTO> register(@Valid @RequestBody RegisterRequest req) {
        return new ResponseEntity<>(userService.register(req), HttpStatus.CREATED);
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest req) {
        return ResponseEntity.ok(userService.login(req));
    }

    @GetMapping("/validate")
    public ResponseEntity<Map<String, Object>> validate(@RequestParam String token) {
        boolean valid = userService.validateToken(token);
        return ResponseEntity.ok(Map.of("valid", valid));
    }
}
