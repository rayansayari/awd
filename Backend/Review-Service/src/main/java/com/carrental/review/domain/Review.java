package com.carrental.review.domain;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "reviews")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class Review {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long userId;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ReviewTargetType targetType;

    @Column(nullable = false)
    private Long targetId;

    @Column(nullable = false)
    private Integer rating; // 1 à 5

    @Column(length = 1000)
    private String comment;

    @Enumerated(EnumType.STRING)
    @Builder.Default
    private ModerationStatus status = ModerationStatus.APPROVED;

    @Builder.Default
    private LocalDateTime createdAt = LocalDateTime.now();
}
