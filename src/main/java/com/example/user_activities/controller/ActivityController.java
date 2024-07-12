package com.example.user_activities.controller;

import com.example.user_activities.model.Activity;
import com.example.user_activities.services.ActivityService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/activities")
public class ActivityController {

    @Autowired
    private ActivityService activityService;

    @PostMapping
    public Mono<ResponseEntity<Activity>> createActivity(@RequestBody Activity activity) {
        if (activity.getAction() == null || activity.getUserId() == null || activity.getBookId() == null) {
            return Mono.just(ResponseEntity.badRequest().build());
        }
        return activityService.saveActivity(activity)
                .map(ResponseEntity::ok)
                .onErrorResume(e -> Mono.just(ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build()));
    }

    @GetMapping("/{id}")
    public Mono<ResponseEntity<Activity>> getActivityById(@PathVariable Long id) {
        return activityService.findById(id)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @GetMapping
    public Flux<Activity> getAllActivities() {
        return activityService.findAll();
    }

    @PutMapping("/{id}")
    public Mono<ResponseEntity<Activity>> updateActivity(@PathVariable Long id, @RequestBody Activity activity) {
        return activityService.updateActivity(id, activity)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public Mono<ResponseEntity<Void>> deleteActivity(@PathVariable Long id) {
        return activityService.deleteActivity(id)
                .then(Mono.fromCallable(() -> ResponseEntity.noContent().<Void>build()))
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }
}
