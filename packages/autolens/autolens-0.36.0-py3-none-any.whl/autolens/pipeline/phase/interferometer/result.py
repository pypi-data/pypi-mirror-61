import numpy as np

import autofit as af
import autoarray as aa
from autoastro.galaxy import galaxy as g
from autolens.pipeline.phase import dataset


class Result(dataset.Result):
    @property
    def most_likely_fit(self):

        hyper_background_noise = self.analysis.hyper_background_noise_for_instance(
            instance=self.instance
        )

        return self.analysis.masked_interferometer_fit_for_tracer(
            tracer=self.most_likely_tracer,
            hyper_background_noise=hyper_background_noise,
        )

    @property
    def real_space_mask(self):
        return self.most_likely_fit.masked_interferometer.real_space_mask

    @property
    def unmasked_model_visibilities(self):
        return self.most_likely_fit.unmasked_blurred_profile_image

    @property
    def unmasked_model_visibilities_of_planes(self):
        return self.most_likely_fit.unmasked_blurred_profile_image_of_planes

    @property
    def unmasked_model_visibilities_of_planes_and_galaxies(self):
        fit = self.most_likely_fit
        return fit.unmasked_blurred_profile_image_of_planes_and_galaxies

    def visibilities_for_galaxy(self, galaxy: g.Galaxy) -> np.ndarray:
        """
        Parameters
        ----------
        galaxy
            A galaxy used in this phase

        Returns
        -------
        ndarray or None
            A numpy arrays giving the model visibilities of that galaxy
        """
        return self.most_likely_fit.galaxy_model_visibilities_dict[galaxy]

    @property
    def visibilities_galaxy_dict(self) -> {str: g.Galaxy}:
        """
        A dictionary associating galaxy names with model visibilities of those galaxies
        """
        return {
            galaxy_path: self.visibilities_for_galaxy(galaxy)
            for galaxy_path, galaxy in self.path_galaxy_tuples
        }

    @property
    def hyper_galaxy_visibilities_path_dict(self):
        """
        A dictionary associating 1D hyper_galaxies galaxy visibilities with their names.
        """

        hyper_galaxy_visibilities_path_dict = {}

        for path, galaxy in self.path_galaxy_tuples:

            hyper_galaxy_visibilities_path_dict[path] = self.visibilities_galaxy_dict[
                path
            ]

        return hyper_galaxy_visibilities_path_dict

    @property
    def hyper_model_visibilities(self):

        hyper_model_visibilities = aa.visibilities.zeros(
            shape_1d=(self.most_likely_fit.visibilities.shape_1d,)
        )

        for path, galaxy in self.path_galaxy_tuples:
            hyper_model_visibilities += self.hyper_galaxy_visibilities_path_dict[path]

        return hyper_model_visibilities

    def image_for_galaxy(self, galaxy: g.Galaxy) -> np.ndarray:
        """
        Parameters
        ----------
        galaxy
            A galaxy used in this phase

        Returns
        -------
        ndarray or None
            A numpy arrays giving the model image of that galaxy
        """
        return self.most_likely_fit.galaxy_model_image_dict[galaxy]

    @property
    def image_galaxy_dict(self) -> {str: g.Galaxy}:
        """
        A dictionary associating galaxy names with model images of those galaxies
        """
        return {
            galaxy_path: self.image_for_galaxy(galaxy)
            for galaxy_path, galaxy in self.path_galaxy_tuples
        }

    @property
    def hyper_galaxy_image_path_dict(self):
        """
        A dictionary associating 1D hyper_galaxies galaxy images with their names.
        """

        hyper_minimum_percent = af.conf.instance.general.get(
            "hyper", "hyper_minimum_percent", float
        )

        hyper_galaxy_image_path_dict = {}

        for path, galaxy in self.path_galaxy_tuples:

            galaxy_image = self.image_galaxy_dict[path]

            if not np.all(galaxy_image == 0):
                minimum_galaxy_value = hyper_minimum_percent * max(galaxy_image)
                galaxy_image[galaxy_image < minimum_galaxy_value] = minimum_galaxy_value

            hyper_galaxy_image_path_dict[path] = galaxy_image

        return hyper_galaxy_image_path_dict

    @property
    def hyper_model_image(self):

        hyper_model_image = aa.masked.array.zeros(mask=self.real_space_mask.mask_sub_1)

        for path, galaxy in self.path_galaxy_tuples:
            hyper_model_image += self.hyper_galaxy_image_path_dict[path]

        return hyper_model_image
