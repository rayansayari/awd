package com.carrental.user.service;

import com.carrental.user.dto.*;
import java.util.List;

public interface UserService {
    UserDTO register(RegisterRequest request);
    AuthResponse login(LoginRequest request);
    UserDTO getUserById(Long id);
    UserDTO updateUser(Long id, RegisterRequest request);
    List<UserDTO> getAllUsers();
    boolean validateToken(String token);
}
