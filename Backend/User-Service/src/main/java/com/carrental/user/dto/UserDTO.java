package com.carrental.user.dto;

import lombok.*;
import java.util.Set;

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class UserDTO {
    private Long id;
    private String username;
    private String email;
    private String firstName;
    private String lastName;
    private String phoneNumber;
    private String driverLicenseNumber;
    private Boolean enabled;
    private Set<String> roles;
}
