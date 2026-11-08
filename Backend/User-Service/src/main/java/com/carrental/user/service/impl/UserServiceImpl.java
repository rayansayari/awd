package com.carrental.user.service.impl;

import com.carrental.user.domain.*;
import com.carrental.user.dto.*;
import com.carrental.user.repository.*;
import com.carrental.user.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {
    private final UserRepository userRepository;
    private final RoleRepository roleRepository;

    @Override
    public UserDTO register(RegisterRequest req) {
        if (userRepository.existsByUsername(req.getUsername())) {
            throw new RuntimeException("Nom d'utilisateur déjà utilisé");
        }
        if (userRepository.existsByEmail(req.getEmail())) {
            throw new RuntimeException("Email déjà enregistré");
        }

        Role clientRole = roleRepository.findByName(RoleName.ROLE_CLIENT)
                .orElseGet(() -> roleRepository.save(Role.builder().name(RoleName.ROLE_CLIENT).description("Client rôle").build()));

        User user = User.builder()
                .username(req.getUsername())
                .email(req.getEmail())
                .password(req.getPassword()) // En production: BCryptPasswordEncoder
                .firstName(req.getFirstName())
                .lastName(req.getLastName())
                .phoneNumber(req.getPhoneNumber())
                .driverLicenseNumber(req.getDriverLicenseNumber())
                .roles(Collections.singleton(clientRole))
                .build();

        User saved = userRepository.save(user);
        return mapToDTO(saved);
    }

    @Override
    public AuthResponse login(LoginRequest req) {
        User user = userRepository.findByUsername(req.getUsernameOrEmail())
                .or(() -> userRepository.findByEmail(req.getUsernameOrEmail()))
                .orElseThrow(() -> new RuntimeException("Identifiants invalides"));

        if (!user.getPassword().equals(req.getPassword())) {
            throw new RuntimeException("Mot de passe incorrect");
        }

        String fakeJwt = "jwt_token_" + Base64.getEncoder().encodeToString(user.getUsername().getBytes());

        return AuthResponse.builder()
                .token(fakeJwt)
                .userId(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .roles(user.getRoles().stream().map(r -> r.getName().name()).collect(Collectors.toList()))
                .build();
    }

    @Override
    public UserDTO getUserById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Utilisateur non trouvé: " + id));
        return mapToDTO(user);
    }

    @Override
    public UserDTO updateUser(Long id, RegisterRequest req) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Utilisateur non trouvé: " + id));
        user.setFirstName(req.getFirstName());
        user.setLastName(req.getLastName());
        user.setPhoneNumber(req.getPhoneNumber());
        user.setDriverLicenseNumber(req.getDriverLicenseNumber());
        return mapToDTO(userRepository.save(user));
    }

    @Override
    public List<UserDTO> getAllUsers() {
        return userRepository.findAll().stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    @Override
    public boolean validateToken(String token) {
        return token != null && token.startsWith("jwt_token_");
    }

    private UserDTO mapToDTO(User u) {
        return UserDTO.builder()
                .id(u.getId())
                .username(u.getUsername())
                .email(u.getEmail())
                .firstName(u.getFirstName())
                .lastName(u.getLastName())
                .phoneNumber(u.getPhoneNumber())
                .driverLicenseNumber(u.getDriverLicenseNumber())
                .enabled(u.getEnabled())
                .roles(u.getRoles().stream().map(r -> r.getName().name()).collect(Collectors.toSet()))
                .build();
    }
}
