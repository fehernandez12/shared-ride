# Shared Ride

Shared Ride is a carpooling platform developed on 2022 as an alternative for Bogotá inhabitants during the years following the COVID-19 Pandemic restrictions, where the car usage is restricted and populations is returning back to normal.

During the environmental contingency we want to encourage people to opt for carpooling within their own communities but most of the information in most carpooling applications is not being adequately gathered. As an immediate solution, we decided to build a very simple application (using Django REST Framework for the backend) to gather and display information about these rides. 

## Development!

You can check the deployment guide [here](https://gist.github.com/pablotrinidad/004122e721bcdc5bd9f0e535a44c7f7e).

To start working on this project I highly recommend you to check
[pydanny's](https://github.com/pydanny) [Django Cookiecutter](https://github.com/pydanny/cookiecutter-django) [documentation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html) on how to get this project up and running locally.
If you don't want to do so, just run:

```bash
docker-compose -f local.yml build
docker-compose -f local.yml up
```

## Contributing

Things that are missing right now:

* [ ] Add tests and coverage implementations
* [ ] Remove weak Token Authorization system
* [ ] Implement more async and periodic tasks to improve the rating system
* [ ] A UI!

## Want to use this project as yours?

Please stick to the [**LICENSE**](LICENSE), you can read a TL;DR
[here](https://tldrlegal.com/license/mit-license).

Again, this is a project I liked a lot and I will love to see it live
again. Feel free to modify, distribute, use privately, etc (READ THE [**LICENSE**](LICENSE)) as
you please just include the Copyright and the [**LICENSE**](LICENSE).

## Contributors

- [Felipe Hernández](https://github.com/fehernandez12)
- [Diego Fino](https://github.com/kiridihos)
- [Juanita Campos](https://github.com/JuanitaCampos1505)

## Special Thanks to

- [Pablo Trinidad](https://github.com/pablotrinidad)
