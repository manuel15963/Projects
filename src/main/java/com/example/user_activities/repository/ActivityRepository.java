package com.example.user_activities.repository;

import com.example.user_activities.model.Activity;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ActivityRepository extends ReactiveCrudRepository<Activity, Long> {
}
