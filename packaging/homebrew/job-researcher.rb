class JobResearcher < Formula
  include Language::Python::Virtualenv

  desc "Local job posting collection, enrichment, and review console"
  homepage "https://github.com/hcscat/job-researcher"
  url "https://github.com/hcscat/job-researcher/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "REPLACE_WITH_RELEASE_SHA256"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  test do
    system bin/"job-researcher", "--help"
  end
end
