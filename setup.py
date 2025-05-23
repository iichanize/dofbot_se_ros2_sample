from setuptools import find_packages, setup

package_name = 'dofbot_se_ros2_sample'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    py_modules=[
        'dofbot_se_ros2_sample.2',
        'dofbot_se_ros2_sample.JointStatePublisher',
    ],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sharp',
    maintainer_email='sharp@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            '2=dofbot_se_ros2_sample.2:main',
            'joint_state_publisher=dofbot_se_ros2_sample.JointStatePublisher:main'
        ],
    },
)
