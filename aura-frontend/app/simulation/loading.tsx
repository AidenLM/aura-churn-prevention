export default function SimulationLoading() {
  return (
    <div className="min-h-screen bg-[#F4F5F7]">
      {/* Header Skeleton */}
      <header className="border-b border-gray-200 bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-8 py-5">
          <div className="w-48 h-8 bg-gray-200 rounded animate-pulse mb-2"></div>
          <div className="w-64 h-4 bg-gray-100 rounded animate-pulse"></div>
        </div>
      </header>

      {/* Main Content Skeleton */}
      <main className="max-w-7xl mx-auto px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Side - Controls Skeleton */}
          <div className="space-y-6">
            {/* Risk Threshold Control */}
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="w-40 h-6 bg-gray-200 rounded animate-pulse mb-6"></div>
              <div className="w-full h-2 bg-gray-200 rounded-full animate-pulse mb-4"></div>
              <div className="flex justify-between">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="w-16 h-3 bg-gray-100 rounded animate-pulse"></div>
                ))}
              </div>
            </div>

            {/* Budget Control */}
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="w-40 h-6 bg-gray-200 rounded animate-pulse mb-6"></div>
              <div className="w-full h-12 bg-gray-100 rounded-lg animate-pulse mb-4"></div>
              <div className="grid grid-cols-3 gap-2">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="h-10 bg-gray-100 rounded-lg animate-pulse"></div>
                ))}
              </div>
            </div>

            {/* Button Skeleton */}
            <div className="w-full h-14 bg-gray-200 rounded-lg animate-pulse"></div>
          </div>

          {/* Right Side - Results Skeleton */}
          <div className="space-y-6">
            {/* Metrics Grid */}
            <div className="grid grid-cols-2 gap-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
                  <div className="w-24 h-4 bg-gray-200 rounded animate-pulse mb-3"></div>
                  <div className="w-32 h-8 bg-gray-200 rounded animate-pulse"></div>
                </div>
              ))}
            </div>

            {/* Additional Metrics */}
            <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
              <div className="w-32 h-5 bg-gray-200 rounded animate-pulse mb-4"></div>
              <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="flex justify-between">
                    <div className="w-40 h-4 bg-gray-200 rounded animate-pulse"></div>
                    <div className="w-24 h-4 bg-gray-200 rounded animate-pulse"></div>
                  </div>
                ))}
              </div>
            </div>

            {/* Coverage Bar */}
            <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
              <div className="w-40 h-5 bg-gray-200 rounded animate-pulse mb-3"></div>
              <div className="w-full h-4 bg-gray-200 rounded-full animate-pulse"></div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
