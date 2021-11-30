# Create VPC
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr_block

  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend: ${terraform.workspace}"
    }
  )
}

# Create internet gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend: ${terraform.workspace}"
    }
  )
}

# Get availability zones
data "aws_availability_zones" "available" {
  state = "available"
}

# Create subnets
resource "aws_subnet" "public_A" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.subnet_public_A_cidr_block
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend Public A: ${terraform.workspace}"
    }
  )
}

resource "aws_subnet" "public_B" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.subnet_public_B_cidr_block
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend Public B: ${terraform.workspace}"
    }
  )
}

resource "aws_subnet" "private_A" {
  count = var.has_private_subnets ? 1 : 0

  vpc_id            = aws_vpc.main.id
  cidr_block        = var.subnet_private_A_cidr_block
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend Private A: ${terraform.workspace}"
    }
  )
}

resource "aws_subnet" "private_B" {
  count = var.has_private_subnets ? 1 : 0

  vpc_id            = aws_vpc.main.id
  cidr_block        = var.subnet_private_B_cidr_block
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend Private B: ${terraform.workspace}"
    }
  )
}

# NAT Gateway
data "aws_ami" "nat_image" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn-ami-vpc-nat*"]
  }

  owners = ["amazon"]
}

resource "aws_instance" "natA" {
  count = var.has_private_subnets ? 1 : 0

  ami                         = data.aws_ami.nat_image.id
  instance_type               = "t3.nano"
  source_dest_check           = false
  subnet_id                   = aws_subnet.public_A.id
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.instance_nat_security_group[count.index].id]

  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend NAT A: ${terraform.workspace}"
    }
  )
}

resource "aws_instance" "natB" {
  count = var.has_private_subnets ? 1 : 0

  ami                         = data.aws_ami.nat_image.id
  instance_type               = "t3.nano"
  source_dest_check           = false
  subnet_id                   = aws_subnet.public_B.id
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.instance_nat_security_group[count.index].id]

  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend NAT B: ${terraform.workspace}"
    }
  )
}

# Route table
resource "aws_default_route_table" "public_route_table" {
  default_route_table_id = aws_vpc.main.default_route_table_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend Public: ${terraform.workspace}"
    }
  )
}

resource "aws_route_table" "private_route_table_A" {
  count = var.has_private_subnets ? 1 : 0

  vpc_id = aws_vpc.main.id

  route {
    cidr_block  = "0.0.0.0/0"
    instance_id = aws_instance.natA[count.index].id
  }

  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend Private A: ${terraform.workspace}"
    }
  )
}

resource "aws_route_table_association" "private_A" {
  count = var.has_private_subnets ? 1 : 0

  subnet_id      = aws_subnet.private_A[count.index].id
  route_table_id = aws_route_table.private_route_table_A[count.index].id
}

resource "aws_route_table" "private_route_table_B" {
  count = var.has_private_subnets ? 1 : 0

  vpc_id = aws_vpc.main.id

  route {
    cidr_block  = "0.0.0.0/0"
    instance_id = aws_instance.natB[count.index].id
  }

  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend Private B: ${terraform.workspace}"
    }
  )
}

resource "aws_route_table_association" "private_B" {
  count = var.has_private_subnets ? 1 : 0

  subnet_id      = aws_subnet.private_B[count.index].id
  route_table_id = aws_route_table.private_route_table_B[count.index].id
}

# Security Groups
resource "aws_security_group" "elb_security_group" {
  vpc_id      = aws_vpc.main.id
  name        = "${var.project}-backend-${terraform.workspace}-elb"
  description = "Security Group for ELB on ${var.project} Backend ${terraform.workspace}"
  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend ELB: ${terraform.workspace}"
    }
  )

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "instances_security_group" {
  vpc_id      = aws_vpc.main.id
  name        = "${var.project}-backend-${terraform.workspace}-instances"
  description = "Security Group for Instances on ${var.project} Backend ${terraform.workspace}"
  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend Instances: ${terraform.workspace}"
    }
  )

  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.elb_security_group.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "rds_security_group" {
  vpc_id      = aws_vpc.main.id
  name        = "${var.project}-backend-${terraform.workspace}-rds"
  description = "Security Group for RDS on ${var.project} Backend ${terraform.workspace}"
  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend RDS: ${terraform.workspace}"
    }
  )

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.instances_security_group.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "instance_nat_security_group" {
  count = var.has_private_subnets ? 1 : 0

  vpc_id      = aws_vpc.main.id
  name        = "${var.project}-backend-${terraform.workspace}-nat"
  description = "Security Group for NAT on ${var.project} Backend ${terraform.workspace}"

  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend NAT: ${terraform.workspace}"
    }
  )

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.vpc_cidr_block]
  }

  # outbound internet access
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "redis_security_group" {
  vpc_id      = aws_vpc.main.id
  name        = "${var.project}-backend-${terraform.workspace}-redis"
  description = "Security Group for Redis on ${var.project} Backend ${terraform.workspace}"
  tags = merge(
    var.common_tags,
    {
      Name : "Walnut Backend Redis: ${terraform.workspace}"
    }
  )

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.instances_security_group.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
