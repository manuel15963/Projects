package pe.edu.vallegrande.project.model;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Data
@Table(name = "Categories")
public class Categories {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "categorias_seq")
    @SequenceGenerator(name = "categorias_seq", sequenceName = "Categorias_seq", allocationSize = 1)
    @Column(name = "category_id")
    private Long id;

    @Column(name = "name")
    private String name;

    @Column(name = "Status")
    private String status; // Puede ser '1' o '0'
}
